"""Discription.

Insta485 explore view.
URLs include:
/explore/

"""
import flask
import insta485
# from insta485.views import util


def get_all_users():
    """Get all users."""
    all_users = []
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * "
        "FROM users "
    )
    results = cur.fetchall()
    for rst in results:
        all_users.append(
            {"username": rst["username"], "user_img_url": rst["filename"]}
        )
    return all_users


def get_not_following(logname):
    """Get not following."""
    following = set()
    not_following = []
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * "
        "FROM following "
        "WHERE username1 = ? ",
        (logname, )
    )
    results = cur.fetchall()
    for rst in results:
        following.add(rst["username2"])
        following.add(logname)
    all_users = get_all_users()
    # print(following)
    for user in all_users:
        # print(f"{user=}")
        # if user["username"] is not logname:
        if user["username"] not in following:
            not_following.append(user)
    return not_following


@insta485.app.route('/explore/', methods=["GET"])
def show_explore():
    """Show explore page."""
    context = {}
    if "username" not in flask.session:
        return flask.redirect(flask.url_for("login"))
    context["logname"] = flask.session["username"]
    context["not_following"] = get_not_following(context["logname"])
    return flask.render_template("explore.html", **context)
