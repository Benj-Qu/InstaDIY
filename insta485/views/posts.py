"""Discription.

Insta485 posts view.
URLs include:
/posts/<postid_url_slug>
/posts/?target=URL

"""
import os
import flask
import arrow
import insta485
from insta485.views import (
    util, target_operation, users
)


def get_post_owner(postid):
    """Get post owner."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT owner "
        "FROM posts "
        "WHERE postid = ? ",
        (postid, )
    )
    result = cur.fetchone()
    return result["owner"]


def get_post_url(postid):
    """Get url of post."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT filename "
        "FROM posts "
        "WHERE postid = ? ",
        (postid, )
    )
    result = cur.fetchone()
    return result["filename"]


# def get_user_img_url(username):
#     """Get url of user img."""
#     connection = insta485.model.get_db()
#     cur = connection.execute(
#         "SELECT filename "
#         "FROM users "
#         "WHERE username = ? ",
#         (username, )
#     )
#     result = cur.fetchone()
#     return result["filename"]


def get_post_timestamp(postid):
    """Get timestamp of post."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT created "
        "FROM posts "
        "WHERE postid = ? ",
        (postid, )
    )
    result = cur.fetchone()
    return arrow.get(result["created"]).humanize()


def get_number_of_likes_post(postid):
    """Get number of likes."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT likeid "
        "FROM likes "
        "WHERE postid = ? ",
        (postid, )
    )
    results = cur.fetchall()
    return len(results)


def get_comments_post(postid):
    """Get comments of post."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * "
        "FROM comments "
        "WHERE postid = ? ",
        (postid, )
    )
    results = cur.fetchall()
    comments = []
    for rst in results:
        data = {}
        data["owner"] = rst["owner"]
        data["text"] = rst["text"]
        data["commentid"] = rst["commentid"]
        comments.append(data)
    return comments


@insta485.app.route('/posts/<postid_url_slug>/', methods=["GET"])
def show_post(postid_url_slug):
    """Show post page."""
    context = {}
    if "username" not in flask.session:
        return flask.redirect(flask.url_for("login"))
    context["logname"] = flask.session["username"]
    context["postid"] = postid_url_slug
    context["owner"] = get_post_owner(postid_url_slug)
    context["owner_img_url"] = users.get_user_img_url(context["owner"])
    context["img_url"] = get_post_url(postid_url_slug)
    context["timestamp"] = get_post_timestamp(postid_url_slug)
    context["likes"] = get_number_of_likes_post(postid_url_slug)
    context["comments"] = get_comments_post(postid_url_slug)
    context["ifliked"] = target_operation.has_liked(context["logname"],
                                                    context["postid"])
    return flask.render_template("post.html", **context)


@insta485.app.route('/posts/', methods=["POST"])
def posts_operation():
    """Post operation."""
    url = flask.request.args.get("target")
    logname = flask.session["username"]
    if url is None:
        url = "/users/" + logname + "/"
    operation = flask.request.form["operation"]
    if operation == "create":
        op_post_create()
    elif operation == "delete":
        op_post_delete()
    return flask.redirect(url)


def op_post_create():
    """Create operation."""
    logname = flask.session["username"]
    # If operation is create, save the image file to disk and redirect to URL
    # If a user tries to create a post with an empty file, then abort(400)
    filename = util.uuid_file()
    if filename:
        connection = insta485.model.get_db()
        connection.execute(
            "INSERT INTO posts(owner, filename)"
            "VALUES (?,?)",
            (logname, filename)
        )
    else:
        flask.abort(400)


def op_post_delete():
    """Discreption.

    If operation is delete, delete the image file
    for postid from the filesystem. Delete everything in
    the database related to this post. Redirect to URL.

    """
    postid = flask.request.form["postid"]
    logname = flask.session["username"]
    if get_post_owner(postid) != logname:
        flask.abort(403)
    else:
        connection = insta485.model.get_db()
        cur = connection.execute(
            "SELECT * FROM posts WHERE postid = ? ",
            (postid, )
        )
        result = cur.fetchone()
        connection.execute(
            "DELETE FROM posts WHERE postid = ? ",
            (postid, )
        )
        connection.commit()
        os.remove(str(insta485.app.config['UPLOAD_FOLDER'])
                  + "/" + result["filename"])
