import requests
import base64
import json
import praw
from datetime import datetime, timedelta

def upload_to_imgur(rqs):
    uri = "https://api.imgur.com/3/image"
    file = rqs.files['file']
    image_string = base64.b64encode(file.read())
    r = requests.post(uri, headers={'Authorization': 'Client-ID 5d513b09dafde5f'}, data=image_string)
    json_r = json.loads(r.content)
    imgur_link = json_r["data"]['link']
    return imgur_link, image_string

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

#convert utc time to a datetime object
def convert_utc_to_datetime(utc_time) -> datetime:
    return datetime.fromtimestamp(utc_time)
    
#get all timestamps within the last 12 hours from an array
def get_last_12_hours(time_array) -> list:
    now = datetime.now()
    last_12_hours = []
    for time in time_array:
        if now - time[0] < timedelta(hours=5):
            last_12_hours.append(time)
    return last_12_hours

#Praw get all posts made by a specific user
def get_all_posts_user(user) -> list:
    reddit = praw.Reddit(
        client_id="dBbawnq6RJY_zdl-TiEoHg",
        client_secret="RWjFvyIseJMGt1hQuKCCQAe-0P_63Q",
        password="Esmeralda1",
        user_agent="script by guy on SO",
        username="swapper_rp",
    )
    posts = reddit.redditor(user).submissions.new(limit=20)
    time_array = []
    for post in posts:
        time_array.append((convert_utc_to_datetime(post.created_utc), post.subreddit))
    return get_last_12_hours(time_array)

def can_i_post_to_bodyswap() -> bool:
    amount_of_bodyswap_posts = 0
    for time_subreddit in get_all_posts_user("swapper_rp"):
        if time_subreddit[1] == "bodyswap":
            amount_of_bodyswap_posts += 1
    if amount_of_bodyswap_posts <= 0:
        return True
    return False

print(can_i_post_to_bodyswap())

def check_rules(caption, subreddit) -> bool:
    x = '{ "status":1, "message": "success"}'
    y = json.loads(x)

    if len(caption) <= 5:
        return json.loads('{"status":0, "message":"tooshort"}')

    if subreddit == "animalswap":
        if caption.find("(IRTR)") != -1:
            return json.loads('{ "status":1, "message": "Success"}')
        else:
            return json.loads('{ "status":0, "message": "Failed, needs to include (IRTR) in string"}')

    if subreddit == "bodyswap":
        if can_i_post_to_bodyswap():
            print("can post")
            return json.loads('{ "status":1, "message": "Success"}')
        else:
            print("cant post")
            return json.loads('{ "status":0, "message": "Failed, you\'ve already posted 3 bodyswap posts"}')
    
    return y
