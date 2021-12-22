"""
Utilities used by the api to publish posts, upload to imgur and get all posts of a user.
"""
import base64
import json
from datetime import datetime, timedelta
import requests
import praw


def upload_to_imgur(rqs):
    """Uploads the image to imgur from a request.

    Args:
        rqs ([type]): The request that contains the image.

    Returns:
        [type]: The link to the image and the image_string.
    """
    uri = "https://api.imgur.com/3/image"
    file = rqs.files["file"]
    image_string = base64.b64encode(file.read())
    post_request = requests.post(
        uri, headers={"Authorization": "Client-ID 5d513b09dafde5f"}, data=image_string
    )
    json_r = json.loads(post_request.content)
    imgur_link = json_r["data"]["link"]
    return imgur_link, image_string


def convert_utc_to_datetime(utc_time) -> datetime:
    """ converts a unix timestamp to a datetimeobject

    Args:
        utc_time ([type]): the input unix timestamp

    Returns:
        datetime: a datetime object
    """
    return datetime.fromtimestamp(utc_time)


def get_last_12_hours(time_array) -> list:
    """Get all the posts from the last 12 hours

    Args:
        time_array ([type]): An array of datetime objects.

    Returns:
        list: The array off posts that have been posted in the last 12 hours.
    """
    now = datetime.now()
    last_12_hours = []
    for time in time_array:
        if now - time[0] < timedelta(hours=12):
            last_12_hours.append(time)
    return last_12_hours


def post_reddit(caption, link, subredditstring):
    """Posts a post to reddit.

    Args:
        caption ([type]): The caption of the post.
        link ([type]): The link to the image.
        subredditstring ([type]): The subreddit to which the post needs to be posted.
    """
    reddit = praw.Reddit(
        client_id="dBbawnq6RJY_zdl-TiEoHg",
        client_secret="RWjFvyIseJMGt1hQuKCCQAe-0P_63Q",
        password="Esmeralda1",
        user_agent="script by guy on SO",
        username="swapper_rp",
    )
    if subredditstring == "FemalePossession":
        subreddit = reddit.subreddit(subredditstring)
        subreddit.submit(
            caption, url=link, flair_id="53eb82f2-9f50-11eb-9d6d-0ec13961dd49"
        )
    else:
        subreddit = reddit.subreddit(subredditstring)
        subreddit.submit(caption, url=link)


def get_all_posts_user(user, testing_array=None) -> list:
    """The function gets all the posts of a user.
    returns a list of tuples with the time and the subreddit.

    Args:
        user ([type]): The user for which the posts need to be fetched.
        testing_array ([type], optional): Is used for testing, you can manually give it a list of
        posts to test. Defaults to None.

    Returns:
        list: A list of tuples with the time and the subreddit.
    """
    reddit = praw.Reddit(
        client_id="dBbawnq6RJY_zdl-TiEoHg",
        client_secret="RWjFvyIseJMGt1hQuKCCQAe-0P_63Q",
        password="Esmeralda1",
        user_agent="script by guy on SO",
        username="swapper_rp",
    )
    if testing_array is not None:
        posts = testing_array
    else:
        posts = reddit.redditor(user).submissions.new(limit=20)
    time_array = []
    for post in posts:
        time_array.append((convert_utc_to_datetime(post.created_utc), post.subreddit))
    return get_last_12_hours(time_array)


def can_i_post_to_bodyswap(testing_array=None) -> bool:
    """The function checks if the user can post to bodyswap.

    Args:
        testing_array ([type], optional): Is used for testing, you can manually give it a list
        of posts. Defaults to None.

    Returns:
        bool: if you can post to bodyswap or not
    """
    amount_of_bodyswap_posts = 0
    for time_subreddit in get_all_posts_user("swapper_rp", testing_array):
        if time_subreddit[1] == "bodyswap":
            amount_of_bodyswap_posts += 1
    if amount_of_bodyswap_posts < 3:
        return True
    return False
