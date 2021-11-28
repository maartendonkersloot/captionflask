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

def get_posts():
    ins_me = f"SELECT * FROM post ORDER BY created DESC LIMIT 20  ;"
    result = get_db().cursor().execute(ins_me)
    return result

def get_post(id):
    ins_me = f"SELECT * FROM post WHERE id ={id};"
    result = get_db().cursor().execute(ins_me)

    return result

def del_post(id):
    cur = get_db().cursor()
    ins_me = f"DELETE FROM post WHERE id ={id};"
    result = cur.execute(ins_me)
    get_db().commit()
    return result

def edit_post(caption, link,posted, id):
    result = get_db().cursor().execute("UPDATE post SET title = ?, link = ?, posted = ? WHERE ID = ?;", (caption, link, posted, id))
    get_db().commit()
    return result