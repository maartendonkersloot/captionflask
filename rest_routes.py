from __main__ import app
from base64 import b64encode
from typing import Type
from db import get_db, insert_post, get_posts, get_post, edit_post, del_post, get__all_posts,get_post_by_link
from flask import request, jsonify, render_template
import json
import base64
import utils

def return_error(erromessage):
    return {"error": erromessage}

@app.route('/api/redditpost', methods=['POST'])
def redditpost():
    args = request.form
    if 'id' not in args:
        return return_error("No id")

    posts = get_post(args['id'])
    for n in posts:   
        if(n[4] == 1):
            return return_error("Already posted")

    first_row = next(posts)
    x = first_row[5].split(",")
    checkrules = True
    messages = []
    for sub in x:
        res = utils.check_rules(first_row[2], sub)
        if res['status'] == 0:
            messages.append(res['message'])
            checkrules = False

    if checkrules == True:
        for sub in x:
             utils.post_reddit(first_row[2], first_row[3], sub)
        edit_post(first_row[2], first_row[3], 1, first_row[0])
    posts = get_post(args['id'])
    jdata = []
    for n in posts:      
        jdata.append({
            "id": n[0],
            "created": n[1],
            "title": n[2],
            "link": n[3],
            "posted": n[4],
            "subreddits": n[5]
            })
    return json.dumps(jdata)
    
    
@app.route('/api/post', methods=['POST'])
def test():
    args = request.form
    if args is None:
        return return_error("No arguments")

    if 'caption' not in args:
        return return_error("No caption")

    if 'subreddits' not in args:
        return return_error("No subreddits")

    if len(args['subreddits']) < 2:
        return return_error("Subreddits too short did you actually include them")

    if 'file' not in request.files:
        return return_error("No fill")

    if len(args['caption']) > 240 or len(args['caption']) < 10:
        return return_error("Caption too long or short, needs to be between 10 and 240")

    file = request.files['file']
    imgur_link, image_string = utils.upload_to_imgur(request)
    file = request.files['file']
    image_stringd = base64.b64encode(file.read())
    post = insert_post(args['caption'], imgur_link, args['subreddits'], image_stringd)
    jdata = []  # create a list
    get_ = get_post_by_link(imgur_link)
    posts = get_.fetchall()
    for n in posts:      
        jdata.append({
            "id": n[0],
            "created": n[1],
            "title": n[2],
            "link": n[3],
            "posted": n[4],
            "subreddits": n[5]
            })
    return json.dumps(jdata)

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

