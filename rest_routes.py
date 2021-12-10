from __main__ import app
from base64 import b64encode
from typing import Type
from db import get_db, insert_post, get_posts, get_post, edit_post, del_post, get__all_posts
from flask import request, jsonify, render_template
import json
@app.route('/test', methods=['GET'])
def test():
    return 'it works!'

@app.route('/api/posts', methods=['GET'])
def posts_get():
    args = request.get_json()
    posts = None
    true_or_false = True
    print(args)
    if args is None:
        true_or_false = False

    if true_or_false == True:
        if 'id' in args and true_or_false == True:
            result = get_post(int(args['id']))
        else:
            if int(args['limit']) > 0:
                if  'order' in args and 'desc' in args:
                    posts = get_posts(int(args['limit']), args['order'], args['desc'])
                elif  'order' not in args and 'desc' in args:
                    posts = get_posts(int(args['limit']), desc=args['desc'])
                elif 'order' in args:
                    posts = get_posts(int(args['limit']), args['order'])
                else:
                    posts = get_posts(int(args['limit']))
            else:
                if  'order' in args and 'desc' in args:
                    posts = get__all_posts(args['order'],  desc=args['desc'])
                elif  'order' not in args and 'desc' in args:
                    posts = get__all_posts( args['desc'])
                elif 'order' in args and not 'desc' in args:
                    posts = get__all_posts(args['order'])
                else:
                    posts = get__all_posts()
            result = posts.fetchall()
    else:
        posts = get__all_posts()
        result = posts.fetchall()

    jdata = []  # create a list

    if true_or_false == False:
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

    for n in result: 
        can_continue = False
        if 'id' not in args or not isinstance(args['id'], list):
            can_continue = True
        else:
            for id in args['id']:
                if id == n[0]:
                    can_continue = True
        if(can_continue):
            dictres = {
                "id": n[0],
                "created": n[1],
                "title": n[2],
                "link": n[3],
                "posted": n[4],
                "subreddits": n[5]
                }
            if 'columns' in args:          
                betterdict = {} 
                for key in args['columns']:
                    if key in dictres:
                        betterdict[key] = dictres[key]
                jdata.append(betterdict)
            else:
                jdata.append(dictres)
    return json.dumps(jdata)

