import base64

import requests
from flask import Flask, request
from flask import render_template
import json
app = Flask(__name__)
import json
import praw
from db import get_db, insert_post, get_posts, get_post, edit_post
from subreddit_custom import SubredditCustom

subreddits = {
    'Bodyswap' : SubredditCustom(['bodyswap'], 'bodyswap'),
    'Possession': SubredditCustom(['Possession'], 'Possession'),
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
    return render_template("index.html", posts=posts, subreddits=subreddits)


@app.route('/', methods=['POST'])
def handle_data():
    caption = request.form['caption']
    imgur_link = upload_to_imgur(request)
    insert_post(caption, imgur_link)
    posts = get_posts()
    return render_template("index.html", posts=posts, subreddits=subreddits)


@app.route('/redditpost', methods=['POST'])
def reddit_post():
    posts = get_post(request.form['data'])
    key = request.form['subs']
    subs = json.loads(key)
    first_row = next(posts)

    for sub in subs:
        post_reddit(first_row[2], first_row[3], sub)
    edit_post(first_row[2], first_row[3], 1, first_row[0])

    posts = get_posts()
    return render_template("index.html", posts=posts, subreddits=subreddits)

@app.route('/editpost', methods=['POST'])
def edit_post_path():
    posts = get_post(request.form['id'])
    caption = request.form['caption']

    for i in posts:
        edit_post(caption, i[3], i[4], i[0])

    posts = get_posts()
    return render_template("index.html", posts=posts, subreddits=subreddits)


def post_reddit(caption, link, subredditstring):
    reddit = praw.Reddit(
        client_id="dBbawnq6RJY_zdl-TiEoHg",
        client_secret="RWjFvyIseJMGt1hQuKCCQAe-0P_63Q",
        password="Esmeralda1",
        user_agent="script by guy on SO",
        username="swapper_rp",
    )
    subreddit = reddit.subreddit(subredditstring)
    subreddit.submit(caption, url=link)


def upload_to_imgur(rqs) -> str:
    uri = "https://api.imgur.com/3/image"
    file = rqs.files['file']
    image_string = base64.b64encode(file.read())
    r = requests.post(uri, headers={'Authorization': 'Client-ID 5d513b09dafde5f'}, data=image_string)
    json_r = json.loads(r.content)
    imgur_link = json_r["data"]['link']
    return imgur_link


if __name__ == '__main__':
    app.run()
