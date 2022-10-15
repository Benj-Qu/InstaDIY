"""REST API for comments."""
import flask
import insta485
from insta485.api.db_operations import own_comment
from insta485.api.utils import *


@insta485.app.route("/api/v1/comments/", methods=["POST"])
def add_comment():
    postid = flask.request.args.get("postid")
    username, has_error, error_code = check_authorization()

    if has_error:
        return flask.jsonify({}), error_code

    if postid_in_range(postid) is False:
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
    return flask.jsonify(**context), 201


@insta485.app.route("/api/v1/comments/<commentid>/", methods=["DELETE"])
def delete_comment(commentid):
    username, has_error, error_code = check_authorization()
    if has_error:
        # 403
        return flask.jsonify({}), error_code
    if commentid_in_range(commentid) is False:
        # if commentid is not in range
        # return 404
        return flask.jsonify({}), 404
    if own_comment(username, commentid) is False:
        return flask.jsonify({}), 403
    connection = insta485.model.get_db()
    connection.execute(
        "DELETE FROM comments WHERE commentid = ? ",
        (commentid, )
    )
    connection.commit()
    return flask.jsonify({}), 204
