"""REST API for comments."""
import flask
import insta485
from insta485.api.db_operations import own_comment, delete_comment_db
from insta485.api.utils import (check_authorization,
                                commentid_in_range,
                                get_error_code)


@insta485.app.route("/api/v1/comments/", methods=["POST"])
def add_comment():
    """Add comment using api."""
    username, _, _ = check_authorization()
    postid = flask.request.args.get("postid")
    if get_error_code(postid):
        return flask.jsonify({}), get_error_code(postid)
    # username, has_error, error_code = check_authorization()

    # if has_error:
    #     return flask.jsonify({}), error_code

    # if postid_in_range(postid) is False:
    #     # if postid is not in range
    #     # return 404
    #     return flask.jsonify({}), 404

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
        "ownerShowUrl": f"/users/{username}/",
        # "ownerShowUrl": "/users/{}/".format(username),
        "text": text,
        "url": f"/api/v1/comments/{commentid}/",
        # "url": "/api/v1/comments/{}/".format(commentid),
    }
    return flask.jsonify(**context), 201


@insta485.app.route("/api/v1/comments/<commentid>/", methods=["DELETE"])
def delete_comment(commentid):
    """Delete comment using api."""
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

    delete_comment_db(commentid)
    # connection = insta485.model.get_db()
    # connection.execute(
    #     "DELETE FROM comments WHERE commentid = ? ",
    #     (commentid, )
    # )
    # connection.commit()
    return flask.jsonify({}), 204
