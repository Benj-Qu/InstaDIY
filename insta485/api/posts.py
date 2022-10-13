"""REST API for posts."""
import math
import flask
import insta485
from insta485.api.utils import check_authorization, postid_in_range

@insta485.app.route('/api/v1/posts/')
def get_posts():

    username, has_error, error_code = check_authorization()
    if has_error:
        return flask.jsonify({}), error_code

    postid_lte = flask.request.args.get("postid_lte", default=math.inf, type=int)
    size = flask.request.args.get("size", default=10, type=int)
    page = flask.request.args.get("page", default=0, type=int)

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

    results = posts[start+size*page:start+size*page+size]
    for result in results:
        result["url"] = "/api/v1/posts/{}/".format(result["postid"])
    if len(results) < size:
        next = ""
    else:
        next = "/api/v1/posts/?size={}&page={}&postid_lte={}".format(size,page+1,postid_lte)

    context = {
        "next": next,
        "results": results,
        "url": flask.request.full_path.rstrip("?")
    }

    return flask.jsonify(**context), 200


@insta485.app.route('/api/v1/posts/<int:postid_url_slug>/')
def get_post(postid_url_slug):
    username, has_error, error_code = check_authorization()
    if has_error:
        return flask.jsonify({}), error_code

    if not postid_in_range(postid_url_slug):
        return flask.jsonify({}), 404

    context = {}
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT commentid, owner, text "
        "FROM comments "
        "WHERE postid = ? "
        "ORDER BY postid ASC",
        (postid_url_slug, )
    )
    raw_comments = cur.fetchall()

    context["comments"] = []
    for raw_comment in raw_comments:
        comment = {}
        comment["commentid"] = raw_comment["commentid"]
        comment["lognameOwnsThis"] = (raw_comment["owner"] == username)
        comment["owner"] = raw_comment["owner"]
        comment["ownerShowUrl"] = "/users/{}/".format(raw_comment["owner"])
        comment["text"] = raw_comment["text"]
        comment["url"] = "/api/v1/comments/{}/".format(raw_comment["commentid"])
        context["comments"] += [comment]

    context["comments_url"] = "/api/v1/comments/?postid={}".format(postid_url_slug)

    cur = connection.execute(
        "SELECT created, filename, owner "
        "FROM posts "
        "WHERE postid = ? ",
        (postid_url_slug, )
    )
    raw_post = cur.fetchone()

    context["created"] = raw_post["created"]
    context["imgUrl"] = "/uploads/{}".format(raw_post["filename"])

    context["likes"] = {}
    cur = connection.execute(
        "SELECT likeid "
        "FROM likes "
        "WHERE owner= ? AND postid = ? ",
        (username, postid_url_slug, )
    )
    logname_like = cur.fetchone()
    context["likes"]["lognameLikesThis"] = (logname_like != None)

    cur = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE postid = ? ",
        (postid_url_slug, )
    )
    raw_likes = cur.fetchall()
    context["likes"]["numLikes"] = len(raw_likes)

    if context["likes"]["lognameLikesThis"]:
        context["likes"]["url"] = "/api/v1/likes/{}/".format(logname_like["likeid"])
    else:
        context["likes"]["url"] = None


    context["owner"] = raw_post["owner"]

    cur = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = ? ",
        (raw_post["owner"], )
    )
    raw_user = cur.fetchone()

    context["ownerImgUrl"] = "/uploads/{}".format(raw_user["filename"])
    context["ownerShowUrl"] = "/users/{}/".format(raw_post["owner"])
    context["postShowUrl"] = "/posts/{}/".format(postid_url_slug)
    context["postid"] = postid_url_slug
    context["url"] = "/api/v1/posts/{}/".format(postid_url_slug)

    return flask.jsonify(**context), 200