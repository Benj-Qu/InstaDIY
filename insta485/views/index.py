"""discription.

Insta485 index (main) view.
URLs include:
/

"""
import os
import flask
import arrow
import insta485
from insta485.views.target_operation import has_liked
from insta485.views import util
# import util


@insta485.app.route('/', methods=["GET"])
def show_index():
    """Show index."""
    if "username" not in flask.session:
        return flask.redirect(flask.url_for("login"))

    context = {}
    connection = insta485.model.get_db()
    context["logname"] = flask.session["username"]
    # context["logname"] = 'awdeorio'

    # logged in user posts information
    cur = connection.execute(
        "SELECT postid, filename AS img_url, owner, created AS timestamp "
        "FROM posts "
        "WHERE owner = ? ",
        (context["logname"], )
    )
    context["posts"] = cur.fetchall()

    # find user following
    cur = connection.execute(
        "SELECT username1, username2 "
        "FROM following "
        "WHERE username1 = ? ",
        (context["logname"], )
    )
    following_list = cur.fetchall()

    # find following users posts information
    for following in following_list:
        cur = connection.execute(
            "SELECT postid, filename AS img_url, owner, created AS timestamp "
            "FROM posts "
            "WHERE owner = ? ",
            (following["username2"], )
        )
        context["posts"] = context["posts"] + cur.fetchall()

    # get followed user photo
    for i, post in enumerate(context["posts"]):
        cur = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = ? ",
            (post["owner"], )
        )
        user_img = cur.fetchall()
        context["posts"][i]["owner_img_url"] = user_img[0]["filename"]

    # get likes & if liked by logname
    cur = connection.execute(
        "SELECT postid, owner "
        "FROM likes ",
    )
    like_list = cur.fetchall()
    for i, _ in enumerate(context["posts"]):
        context["posts"][i]["likes"] = 0
        context["posts"][i]["ifliked"] = \
            has_liked(context["logname"], context["posts"][i]["postid"])
        # print(context["posts"][i]["ifliked"])
        for like in like_list:
            if like["postid"] == context["posts"][i]["postid"]:
                context["posts"][i]["likes"] += 1
                # if like["owner"] == context["logname"]:
                #     context["posts"][i]["ifliked"] = True

    # get comments
    for i, post in enumerate(context["posts"]):
        cur = connection.execute(
            "SELECT owner, text "
            "FROM comments "
            "WHERE postid = ? ",
            (post["postid"], )
        )
        comments = cur.fetchall()
        context["posts"][i]["comments"] = comments

    # fix timestamp
    for i, _ in enumerate(context["posts"]):
        context["posts"][i]["timestamp"] = \
            arrow.get(context["posts"][i]["timestamp"]).humanize()

    # sort by postid
    context["posts"].sort(key=lambda d: d['postid'], reverse=True)
    return flask.render_template("index.html", **context)


@insta485.app.route('/uploads/<path:filename>')
# @util.require_login()_403
@util.require_login(False)
def find_file(filename):
    """Find file."""
    path = str(insta485.app.config['UPLOAD_FOLDER']) + '/' + filename
    if not os.path.exists(path):
        # print("1111111111")
        flask.abort(404)
    return flask.send_from_directory(insta485.app.config['UPLOAD_FOLDER'],
                                     filename, as_attachment=True)
