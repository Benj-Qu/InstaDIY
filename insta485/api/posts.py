"""REST API for posts."""
import flask
import insta485
import hashlib
import arrow

@insta485.app.route('/api/v1/posts/')
def get_posts_without_size():
    if flask.request.authorization:
        username = flask.request.authorization['username']
        password = flask.request.authorization['password']
    context = get_posts(username)
    
    return flask.jsonify(**context)


@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post(postid_url_slug):
    """Return post on postid.
    Example:
    {
        "created": "2017-09-28 04:33:28",
        "imgUrl": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
        "owner": "awdeorio",
        "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
        "ownerShowUrl": "/users/awdeorio/",
        "postShowUrl": "/posts/1/",
        "url": "/api/v1/posts/1/"
    }
    """
    context = {
        "created": "2017-09-28 04:33:28",
        "imgUrl": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
        "owner": "awdeorio",
        "ownerImgUrl": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
        "ownerShowUrl": "/users/awdeorio/",
        "postid": "/posts/{}/".format(postid_url_slug),
        "url": flask.request.path,
    }
    return flask.jsonify(**context)

def get_posts(usr, n = 10):
    posts = []
    connection = insta485.model.get_db()

    # posts of the user
    cur = connection.execute(
        "SELECT postid"
        "FROM posts "
        "WHERE owner = ? ",
        (usr, )
    )
    posts = cur.fetchall()

    # posts of following users
    cur = connection.execute(
        "SELECT username1, username2 "
        "FROM following "
        "WHERE username1 = ? ",
        (usr, )
    )
    following_list = cur.fetchall()

    for following in following_list:
        cur = connection.execute(
            "SELECT postid, filename AS img_url, owner, created AS timestamp "
            "FROM posts "
            "WHERE owner = ? ",
            (following["username2"], )
        )
        posts += cur.fetchall()
    
    # fix timestamp
    for i, _ in enumerate(posts):
        posts[i]["timestamp"] = \
            arrow.get(posts[i]["timestamp"]).humanize()

    # sort by postid
    posts.sort(key=lambda d: d['postid'], reverse=True)
    
    context = {
        "next": "",
        "results": posts[:n],
        "url": "/api/v1/posts/"
    }
    context["next"] = "" 
    context["results"] = get_posts(username)