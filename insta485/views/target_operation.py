"""Discription.

Insta485 posts view.
URLs include:
/likes/?target=URL
/comments/?target=URL
/following/?target=URL

"""
import flask
import insta485
from insta485.views.users import is_following


# def is_following(username1, username2):
#     """If is following."""
#     # if username1 follows username2, return True
#     # else return False
#     if username1 == username2:
#         return False
#     connection = insta485.model.get_db()
#     cur = connection.execute(
#         "SELECT * "
#         "FROM following "
#         "WHERE username1 = ? AND username2 = ?",
#         (username1, username2)
#     )
#     return len(cur.fetchall()) != 0


def has_liked(username, postid):
    """If has liked."""
    # Return True if username has already liked this postid
    # else return False
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE owner = ? AND postid = ?",
        (username, postid)
    )
    return len(cur.fetchall()) != 0


def get_likeid(username, postid):
    """Get likeid."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT likeid "
        "FROM likes "
        "WHERE owner = ? AND postid = ?",
        (username, postid, )
    )
    results = cur.fetchone()
    return results["likeid"]


def find_comment_owner(commentid):
    """Find comment owner."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT owner "
        "FROM comments "
        "WHERE commentid = ? ",
        (commentid, )
    )
    results = cur.fetchone()
    return results["owner"]


@insta485.app.route('/likes/', methods=["POST"])
def likes_operation():
    """Likes."""
    url = flask.request.args.get("target")
    if not url:
        url = flask.url_for("show_index")
    operation = flask.request.form["operation"]
    if operation == "like":
        op_like()
    elif operation == "unlike":
        op_unlike()
    return flask.redirect(url)


def op_like():
    """Like the post."""
    logname = flask.session["username"]
    postid = flask.request.form["postid"]
    if has_liked(logname, postid):
        flask.abort(409)
    connection = insta485.model.get_db()
    connection.execute(
        "INSERT INTO likes(owner, postid) "
        "VALUES (?, ?) ",
        (logname, postid, )
    )
    connection.commit()


def op_unlike():
    """Unlike the post."""
    postid = flask.request.form["postid"]
    logname = flask.session["username"]
    if not has_liked(logname, postid):
        flask.abort(409)
    connection = insta485.model.get_db()
    connection.execute(
        "DELETE FROM likes WHERE likeid = ? ",
        (get_likeid(logname, postid), )
    )
    connection.commit()


@insta485.app.route('/comments/', methods=["POST"])
def comments_operation():
    """Comments."""
    url = flask.request.args.get("target")
    if not url:
        url = flask.url_for("show_index")

    operation = flask.request.form["operation"]
    if operation == "create":
        op_create()
    elif operation == "delete":
        op_delete()
    return flask.redirect(url)


def op_create():
    """Create comment."""
    postid = flask.request.form["postid"]
    text = flask.request.form["text"]
    logname = flask.session["username"]
    if text:
        connection = insta485.model.get_db()
        connection.execute(
            "INSERT INTO comments(owner, postid, text) "
            "VALUES (?, ?, ?) ",
            (logname, postid, text, )
            )
        connection.commit()
    else:
        flask.abort(400)


def op_delete():
    """Delete comment."""
    commentid = flask.request.form["commentid"]
    logname = flask.session["username"]
    if logname != find_comment_owner(commentid):
        flask.abort(403)
    connection = insta485.model.get_db()
    connection.execute(
        "DELETE FROM comments WHERE commentid = ? ",
        (commentid, )
    )
    connection.commit()


@insta485.app.route('/following/', methods=["POST"])
def following_operation():
    """Following."""
    url = flask.request.args.get("target")
    if not url:
        url = flask.url_for("show_index")
    operation = flask.request.form["operation"]
    if operation == "follow":
        op_follow()
    elif operation == "unfollow":
        op_unfollow()
    return flask.redirect(url)


def op_follow():
    """Follow."""
    username = flask.request.form["username"]
    # print(username)
    logname = flask.session["username"]
    # print(logname)
    # If a user tries to follow a user that
    # they already follow or unfollow a user that they do not follow,
    # then abort(409).
    if is_following(logname, username):
        flask.abort(409)
    connection = insta485.model.get_db()
    connection.execute(
            "INSERT INTO following(username1, username2) "
            "VALUES (?, ?) ",
            (logname, username, )
        )
    connection.commit()


def op_unfollow():
    """Unfollow."""
    username = flask.request.form["username"]
    logname = flask.session["username"]
    # If a user tries to follow a user that
    # they already follow or unfollow a user that they do not follow,
    # then abort(409).
    if not is_following(logname, username):
        flask.abort(409)
    connection = insta485.model.get_db()
    connection.execute(
        "DELETE FROM following WHERE username1 = ? AND username2 = ? ",
        (logname, username,)
    )
    connection.commit()
