import base64

import requests
from flask import Flask, request,jsonify
from flask import render_template
import json

app = Flask(__name__)
import json
import praw
from db import get_db, insert_post, get_posts, get_post, edit_post, del_post
from subreddit_custom import SubredditCustom
import os
import PIL.Image

import base64

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


@app.route('/')
def hello_world():  # put application's code here
    # init_db()
    get_db().cursor()
    posts = get_posts()
    return render_template("index.html", posts=posts, posts_copy=posts, subreddits=subreddits)


@app.route('/browse')
def browse():  # put application's code here
    # Import the os module

    # Get the current working directory
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
    posts = get_posts()
    return render_template("for.html", posts=posts, posts_copy=posts, subreddits=subreddits)


@app.route('/', methods=['POST'])
def handle_data():
    caption = request.form['caption']
    subredditsdds = request.form['subreddits']
    imgur_link, image_string = upload_to_imgur(request)
    file = request.files['file']
    image_stringd = base64.b64encode(file.read())
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
        res = check_rules(first_row[2], sub)
        if res['status'] == 0:
            messages.append(res['message'])
            checkrules = False

    if checkrules == True:
        for sub in x:
            post_reddit(first_row[2], first_row[3], sub)
        edit_post(first_row[2], first_row[3], 1, first_row[0])

    posts = get_posts()
    return render_template("for.html", posts=posts, posts_copy=posts, subreddits=subreddits, messages=messages)


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


def post_reddit(caption, link, subredditstring):
    reddit = praw.Reddit(
        client_id="dBbawnq6RJY_zdl-TiEoHg",
        client_secret="RWjFvyIseJMGt1hQuKCCQAe-0P_63Q",
        password="Esmeralda1",
        user_agent="script by guy on SO",
        username="swapper_rp",
    )
    if (subredditstring == "FemalePossession"):
        subreddit = reddit.subreddit(subredditstring)
        subreddit.submit(caption, url=link, flair_id="53eb82f2-9f50-11eb-9d6d-0ec13961dd49")
    else:
        subreddit = reddit.subreddit(subredditstring)
        subreddit.submit(caption, url=link)


def upload_to_imgur(rqs):
    uri = "https://api.imgur.com/3/image"
    file = rqs.files['file']
    image_string = base64.b64encode(file.read())
    r = requests.post(uri, headers={'Authorization': 'Client-ID 5d513b09dafde5f'}, data=image_string)
    json_r = json.loads(r.content)
    imgur_link = json_r["data"]['link']
    return imgur_link, image_string


def check_rules(caption, subreddit):
    x = '{ "status":1, "message": "success"}'
    y = json.loads(x)

    if len(caption) <= 5:
        return json.loads('{"status":0, "message":"tooshort"}')

    if subreddit == "animalswap":
        if caption.find("(IRTR)") != -1:
            return json.loads('{ "status":1, "message": "Success"}')
        else:
            return json.loads('{ "status":0, "message": "Failed, needs to include (IRTR) in string"}')

    return y


if __name__ == '__main__':
    app.run(host="0.0.0.0")
