"""
The api routes for the api.
"""
import json
from db import Db
from flask import request, render_template
from flask import Blueprint
from config import get_api_key

db = Db()
db.create_db()
api_routes = Blueprint("api_routes", __name__)


@api_routes.route("/api/posts", methods=["GET"])
def posts_get():
    """
    Gets all the posts in the database
    Returns:
        [type]: A json off the posts in the database
    """
    return db.get_posts()


@api_routes.route("/api/posts/js", methods=["GET"])
def post_posts_posts():
    """
    Posts a post to the subreddit
    Returns:
        [type]: Returns the for html template with the posts and api key included
    """
    posts = db.get_posts()
    return render_template("for.html", posts=json.loads(posts), api=get_api_key())


@api_routes.route("/api/posts", methods=["POST"])
def posts_post():
    """
    Posts a post to the database
    Returns:
        [type]: Returns the posted post
    """
    print(request.form)
    return db.add_post(request)


@api_routes.route("/api/posts/<id>", methods=["GET"])
def posts_get_by_id(post_id):
    """
    Get a post by id
    Args:
        id ([type]): id of the post to get

    Returns:
        [type]: a json of the post
    """
    return db.get_post_by_id(post_id)


@api_routes.route("/api/posts/<id>", methods=["PUT"])
def posts_update(id):
    """
    Updates a post by id
    Args:
        post_id ([type]): The id of the post to update

    Returns:
        [type]: The updated post
    """
    return db.update_post(id, request.form)


@api_routes.route("/api/posts/<id>", methods=["DELETE"])
def posts_delete(id):
    """
    Deletes a post by id
    Args:
        post_id ([type]): id of the post to delete

    Returns:
        [type]: a json of the result
    """
    print(id)
    return db.delete_post_by_id(id)


@api_routes.route("/api/posts/post/<id>", methods=["POST"])
def posts_post_to_reddit(id):
    """
    Post a post to reddit by id
    Args:
        post_id ([type]): id of the post to post

    Returns:
        [type]: a json of the result
    """
    return db.post_post_to_reddit(id)
