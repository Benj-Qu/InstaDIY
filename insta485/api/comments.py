"""REST API for comments."""
from crypt import methods
from multiprocessing import context
import flask
import insta485
from insta485.api.utils import *

@insta485.app.route("/api/v1/comments/", methods=["POST"])
def add_comment():
    postid = flask.request.args.get("postid")
    username, has_error, error_code = check_authorization()
    
    if has_error:
        return flask.jsonify({}), error_code
    
    if postid_in_range(postid) == False:
        # if postid is not in range
        # return 404
        return flask.jsonify({}), 404
    
    text = flask.request.get_json()["text"]
    connection = insta485.model.get_db()
    connection.execute(
        "INSERT INTO comments(owner, postid, text) "
        "VALUES (?, ?, ?) ",
        (username, postid, text, )
    )
    connection.commit()
    cur = connection.execute(
        "SELECT last_insert_rowid() AS id "
        "FROM comments ",
    )
    commentid = cur.fetchone()["id"]
    context = {
        "commentid": commentid,
        "lognameOwnsThis": True,
        "owner": username,
        "ownerShowUrl": "/users/{}/".format(username),
        "text": text,
        "url": "/api/v1/comments/{}/".format(commentid),
    }
    