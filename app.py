from flask import Flask
from secrets import token_urlsafe
import datetime
import json


app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello, World!"

@app.post('/<msg>/<reply_id>')
def create_post(msg, reply_id="none"):
    if msg != isinstance(str):
        return { 'err': 'msg not a string or missing msg' }, 400
    
    if len(forum_posts) == 0:
        id = 0
    else:
        id = forum_posts[len(forum_posts) - 1]["id"] + 1
    
    key = token_urlsafe(16)
    timestamp = datetime.datetime.now().timestamp()


    post = {
        "id": id,
        "key": key,
        "timestamp": timestamp,
        "msg": msg,
        "reply": reply_id
    }

    with open("forum.json", "w") as outfile:
        json.dump(post, outfile)

    return

@app.route('/<id>', methods=['GET'])
def get_post(id):
    for item in forum_posts:
        if forum_posts[item]["id"] == id:
            return forum_posts[item]

    return { 'err': 'id not found' }, 400

@app.delete('/<id>/<key>')
def delete_post(id, key):
    for item in forum_posts:
        if forum_posts[item]["id"] == id and forum_posts[item]["key"] == key:
            deleted_post = forum_posts[item]
            forum_posts.pop(item)
            return deleted_post
        elif forum_posts[item]["id"] == id and forum_posts[item]["key"] != key:
            return { 'err': 'forbidden' }, 403
    
    return { 'err': 'Not found' }, 404


if __name__ == "__main__":
    with open('forum.json', 'r', encoding="utf8") as postfile:
        forum_posts = json.load(postfile)
    with open('users.json', 'r', encoding="utf8") as userdata:
        users = json.load(userdata)

    app.run(debug=True)
