from __main__ import app
from db import Db
from flask import request, jsonify, render_template
import json

db = Db()
import sys
from config import get_api_key

db.create_db()


@app.route("/api/posts", methods=["GET"])
def posts_get():
    print(sys.argv[0])
    return db.get_posts()


@app.route("/api/posts/js", methods=["GET"])
def post_posts_posts():
    posts = db.get_posts()
    return render_template("for.html", posts=json.loads(posts), api=get_api_key())


@app.route("/api/posts", methods=["POST"])
def posts_post():
    print(request.form)
    return db.add_post(request)


@app.route("/api/posts/<id>", methods=["GET"])
def posts_get_by_id(id):
    return db.get_post_by_id(id)


@app.route("/api/posts/<id>", methods=["PUT"])
def posts_update(id):
    return db.update_post(id, request.form)


@app.route("/api/posts/<id>", methods=["DELETE"])
def posts_delete(id):
    return db.delete_post_by_id(id)


@app.route("/api/posts/post/<id>", methods=["POST"])
def posts_post_to_reddit(id):
    return db.post_post_to_reddit(id)

