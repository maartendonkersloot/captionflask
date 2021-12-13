import base64
from db import get_db, insert_post, get_posts, get_post, edit_post, del_post, insert_post_datetime, get__all_posts
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
import json
import os
import praw
import requests
from subreddit_custom import SubredditCustom
import rest_routes
import utils
from datetime import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import time
subreddits = {
    'Bodyswap': SubredditCustom(['bodyswap'], 'bodyswap'),
    'FemalePossession': SubredditCustom(['FemalePossession'], 'FemalePossession'),
    'animalswap': SubredditCustom(['animalswap'], 'animalswap'),
    'AnimePossession': SubredditCustom(['AnimePossession'], 'AnimePossession'),
    'BodySwapRP': SubredditCustom(['BodySwapRP'], 'BodySwapRP'),
    'CelebSwap': SubredditCustom(['CelebSwap'], 'CelebSwap'),
    'MinorityBodySwap': SubredditCustom(['MinorityBodySwap'], 'MinorityBodySwap'),
    'FictionBodySwap': SubredditCustom(['FictionBodySwap'], 'FictionBodySwap'),
}

def get_posts_local(limit = 20):
    posts = get_posts(limit)
    postswithoutsched = []
    scheduled = []
    for post in posts.fetchall():
        if post[7] == None or post[7] == 0:
            postswithoutsched.append(post)
        else:
            scheduled.append(post)
    return postswithoutsched, scheduled

@app.route('/')
def hello_world():  # put application's code here
    get_db().cursor()
    posts, scheduled = get_posts_local(20)
    return render_template("index.html", posts=posts,scheduled=scheduled, posts_copy=posts, subreddits=subreddits)


@app.route('/browse')
def browse(): 
    cwd = os.getcwd()
    my_list = os.listdir(cwd)
    print("Current working directory: {0}".format(cwd))
    print(my_list)
    images = findandreturnimages(cwd)
    return render_template("browse.html", currentdir=cwd, currentfiles=my_list, images=images)

def findandreturnimages(dir):
    my_list = os.listdir(dir)
    list = []
    for items in my_list:
        string = dir +"/"+ str(items)
        if items.endswith('.png') == True:
            with open(string, "rb") as img_file:
                my_string = base64.b64encode(img_file.read()).decode('utf-8')
            list.append(my_string)
        if items.endswith('.jpg') == True:
            with open(string, "rb") as img_file:
                my_string = base64.b64encode(img_file.read()).decode('utf-8')
            list.append(my_string)
        if items.endswith('.JPG') == True:
            with open(string, "rb") as img_file:
                my_string = base64.b64encode(img_file.read()).decode('utf-8')
            list.append(my_string)
    return list

@app.route('/dir', methods=['POST'])
def getdir_up():
    dirr = request.form['dir']
    path_parent = os.path.dirname(dirr)
    my_list = os.listdir(path_parent)
    images = findandreturnimages(path_parent)
    return jsonify(currentdir=path_parent, currentfiles=my_list, images=images)

@app.route('/dirdown', methods=['POST'])
def getdir_down():
    dirr = request.form['dir']
    fileordir = request.form['fileordir']
    path = dirr + "/" + fileordir
    my_list = os.listdir(path)
    images = findandreturnimages(path)
    return jsonify(currentdir=path, currentfiles=my_list, images=images)

def return_main():
    posts,scheduled = get_posts_local(20)
    return render_template("for.html", posts=posts,scheduled=scheduled, posts_copy=posts, subreddits=subreddits)


@app.route('/', methods=['POST'])
def handle_data():
    caption = request.form['caption']
    datetimepicker = request.form['datetimepicker']
    subredditsdds = request.form['subreddits']
    imgur_link, image_string = utils.upload_to_imgur(request)
    file = request.files['file']
    image_stringd = base64.b64encode(file.read())
    print(datetimepicker)
    if datetimepicker != 0:
        insert_post_datetime(caption, imgur_link, subredditsdds, image_stringd, datetimepicker)
    else:
        insert_post(caption, imgur_link, subredditsdds, image_stringd)
    return return_main()


@app.route('/get', methods=['POST'])
def get_postss():
    return return_main()


@app.route('/redditpost', methods=['POST'])
def reddit_post():
    posts = get_post(request.form['data'])
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

    posts,scheduled = get_posts_local(20)
    return render_template("for.html", posts=posts,scheduled=scheduled, posts_copy=posts, subreddits=subreddits, messages=messages)

def run_hourly():
    with app.app_context():
        print("Check scheduled posts")
        get_db().cursor()
        posts = get__all_posts()
        for post in posts:
            if post[7] != None and post[7] != 0 and post[4] == 0:
                datetime_object = datetime.strptime(post[7][:23], '%Y/%m/%d %H:%M')
                if datetime_object < datetime.now():
                    x = post[5].split(",")
                    for sub in x:
                        print("posting to " + sub)
                        utils.post_reddit(post[2], post[3], sub)
                    edit_post(post[2], post[3], 1, post[0])

@app.route('/deletepost', methods=['POST'])
def delete_post():
    del_post(request.form['id'])
    return return_main()


@app.route('/editpost', methods=['POST'])
def edit_post_path():
    posts = get_post(request.form['id'])
    caption = request.form['caption']
    for i in posts:
        edit_post(caption, i[3], i[4], i[0])
    return return_main()

with app.app_context():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=run_hourly, trigger="interval", minutes=15)
    scheduler.start()


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
    