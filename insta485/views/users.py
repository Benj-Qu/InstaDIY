"""Discription.

Insta485 users view.
URLs include:
/users/<user_url_slug>/
/users/<user_url_slug>/follower
/users/<user_url_slug>/following

"""
import flask
import insta485
from insta485.views import util


def is_following(username1, username2):
    """If is following."""
    # if username1 follows username2, return True
    # else return False
    if username1 == username2:
        return False
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * "
        "FROM following "
        "WHERE username1 = ? AND username2 = ?",
        (username1, username2)
    )
    return len(cur.fetchall()) != 0


def get_fullname(username):
    """Get full name from database where username is username."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT fullname "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    result = cur.fetchone()
    return result["fullname"]


def get_following_number(username):
    """Get following number."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 = ? ",
        (username, )
    )
    result = cur.fetchall()
    return len(result)


def get_follower_number(username):
    """Get follower number."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT username1 "
        "FROM following "
        "WHERE username2 = ? ",
        (username, )
    )
    result = cur.fetchall()
    return len(result)


def get_total_posts_number(username):
    """Get total posts number."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT postid "
        "FROM posts "
        "WHERE owner = ? ",
        (username, )
    )
    result = cur.fetchall()
    return len(result)


def get_posts(username):
    """Get posts."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT postid, filename "
        "FROM posts "
        "WHERE owner = ? ",
        (username, )
    )
    result = cur.fetchall()
    posts = []
    for rst in result:
        posts.append({"postid": str(rst["postid"]),
                      "img_url": rst["filename"]})
    return posts


def user_url_slug_not_in_db(user_url_slug):
    """Return true if user_url_slug does not exist in database."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * "
        "FROM users "
        "WHERE username = ? ",
        (user_url_slug, )
    )
    result = cur.fetchone()
    if result is None:
        return True
    return False


def get_followers(username):
    """Get followers."""
    followers = []
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT username1 "
        "FROM following "
        "WHERE username2 = ? ",
        (username, )
    )
    result = cur.fetchall()
    for rst in result:
        followers.append({
            "username": rst["username1"],
            "user_img_url": get_user_img_url(rst["username1"]),
            "logname_follows_username":
                is_following(username, rst["username1"])
        })
    return followers


def get_user_img_url(username):
    """Get url of user img."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    result = cur.fetchone()
    return result["filename"]


def get_following(username):
    """Get following."""
    following = []
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 = ? ",
        (username, )
    )
    result = cur.fetchall()
    for rst in result:
        following.append({
            "username": rst["username2"],
            "user_img_url": get_user_img_url(rst["username2"]),
            "logname_follows_username":
                is_following(username, rst["username2"])
        })
    return following


@insta485.app.route('/users/<user_url_slug>/', methods=["GET"])
@util.require_login()
def show_user(user_url_slug):
    """Show user page."""
    if user_url_slug_not_in_db(user_url_slug):
        flask.abort(404)
    context = {}
    context["logname"] = flask.session["username"]
    # DELETE
    # context["logname"] = user_url_slug
    context['username'] = user_url_slug
    context['user_url_slug'] = user_url_slug
    # DELETE
    context["logname_follows_username"] = \
        is_following(context["logname"], context["username"])
    context["fullname"] = get_fullname(context["username"])
    context["following"] = get_following_number(context['username'])
    context["followers"] = get_follower_number(context['username'])
    context["total_posts"] = get_total_posts_number(context['username'])
    context["posts"] = get_posts(context['username'])
    return flask.render_template("user.html", **context)


@insta485.app.route('/users/<user_url_slug>/followers/', methods=["GET"])
@util.require_login()
def show_follower(user_url_slug):
    """Show follower."""
    if user_url_slug_not_in_db(user_url_slug):
        flask.abort(404)
    context = {}
    # if "username" not in flask.session:
    #     return flask.redirect(flask.url_for("login"))
    context["logname"] = flask.session["username"]
    context['username'] = user_url_slug
    context["followers"] = get_followers(user_url_slug)
    return flask.render_template("followers.html", **context)


@insta485.app.route('/users/<user_url_slug>/following/', methods=["GET"])
@util.require_login()
def show_following(user_url_slug):
    """Show following."""
    if user_url_slug_not_in_db(user_url_slug):
        flask.abort(404)
    context = {}
    # if "username" not in flask.session:
    #     return flask.redirect(flask.url_for("login"))
    context["logname"] = flask.session["username"]
    context['username'] = user_url_slug
    context["following"] = get_following(user_url_slug)
    return flask.render_template("following.html", **context)
