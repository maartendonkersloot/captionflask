from __main__ import app
from base64 import b64encode
from db import get_db, insert_post, get_posts, get_post, edit_post, del_post
from flask import request, jsonify, render_template
import json
@app.route('/test', methods=['GET'])
def test():
    return 'it works!'

@app.route('/api/posts', methods=['GET'])
def posts_get():
    posts_cursor = get_posts()
    print(type(posts_cursor))
    result = posts_cursor.fetchall()
    print(type(result))
    jdata = []  # create a list
    for n in result:                
        jdata.append({
            "id": n[0],
            "created": n[1],
            "title": n[2],
            "link": n[3],
            "posted": n[4],
            "subreddits": n[5]
            })
    return json.dumps(jdata)

