import sqlite3
from flask import current_app, g
DATABASE = 'database.db'

def init_db():
    db = get_db()

    with current_app.open_resource('scheme.sql') as f:
        db.executescript(f.read().decode('utf8'))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def close_connection():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def insert_post(caption, link, subreddits, image):
    result = get_db().cursor().execute("INSERT INTO post (title, link, subreddits,image,posted ) VALUES (?, ?, ?,?,0);", (caption, link, subreddits, image))
    get_db().commit()
    return result

def insert_post_datetime(caption, link, subreddits, image, datetime):
    result = get_db().cursor().execute("INSERT INTO post (title, link, subreddits,image, scheduled,posted ) VALUES (?, ?, ?,?,?,0);", (caption, link, subreddits, image,datetime))
    get_db().commit()
    return result

def get_posts(limit, order = "created", desc = "DESC"):
    ins_me = f"SELECT * FROM post ORDER BY {order} {desc} LIMIT {limit};"
    result = get_db().cursor().execute(ins_me)
    return result

def get_scheduled(sched, order = "created", desc = "DESC"):
    ins_me = f"SELECT * FROM post WHERE scheduled = {sched} ORDER BY {order} {desc} ;"
    result = get_db().cursor().execute(ins_me)
    return result

def get__all_posts(order = "created", desc = "DESC"):
    ins_me = f"SELECT * FROM post ORDER BY {order} {desc};"
    result = get_db().cursor().execute(ins_me)
    return result

def get_post(id):
    ins_me = f"SELECT * FROM post WHERE id ={id};"
    result = get_db().cursor().execute(ins_me)
    return result

def get_post_by_link(link):
    print
    result = get_db().cursor().execute(f"SELECT * FROM post WHERE link = '{link}';")
    return result

def del_post(id):
    cur = get_db().cursor()
    ins_me = f"DELETE FROM post WHERE id ={id};"
    result = cur.execute(ins_me)
    get_db().commit()
    return result

def edit_post(caption, link,posted, id, scheduled):
    result = get_db().cursor().execute("UPDATE post SET title = ?, link = ?, posted = ?, scheduled = ? WHERE ID = ?;", (caption, link, posted, id,scheduled))
    get_db().commit()
    return result