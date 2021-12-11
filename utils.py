import requests
import base64
import json
import praw
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
