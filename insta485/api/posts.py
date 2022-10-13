"""REST API for posts."""
import math
import flask
import insta485
import hashlib
import arrow
from insta485.api.utils import check_authorization

@insta485.app.route('/api/v1/posts/')
def get_posts():
    
    username, has_error, error_code = check_authorization()
    if has_error:
        return flask.jsonify({}), error_code

    postid_lte = flask.request.args.get("postid_lte", default=math.inf, type=int)
    size = flask.request.args.get("size", default=10, type=int)
    page = flask.request.args.get("page", default=1, type=int)

    if size < 0 or page < 0:
        return flask.jsonify({}), 400

    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT postid "
        "FROM posts "
        "WHERE (owner = ?) OR "
        "(owner IN (SELECT username2 FROM following WHERE username1 = ?)) "
        "ORDER BY postid DESC",
        (username, username, )
    )
    posts = cur.fetchall()

    if postid_lte == math.inf:
        postid_lte = posts[0]["postid"]
    
    for i, post_dict in enumerate(posts):
        if post_dict["postid"] <= postid_lte:
            start = i
            break

    context = {}
    context["next"] = "/api/v1/posts/?size={}&page={}&postid_lte={}".format(size,page+1,postid_lte)
    context["results"] = posts[start+size*page:start+size*page+size]
    context["url"] = flask.request.full_path
    
    return flask.jsonify(**context), 200


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
    return flask.jsonify(**context), 200