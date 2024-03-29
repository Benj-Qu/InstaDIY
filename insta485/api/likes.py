"""REST API for likes."""
import flask
import insta485
from insta485.api.utils import (check_authorization,
                                get_error_code)
from insta485.api.db_operations import (has_liked,
                                        get_likeid,
                                        own_like, likeid_exists)


@insta485.app.route('/api/v1/likes/', methods=["POST"])
def create_like():
    """Add like using api."""
    username, _, _ = check_authorization()
    postid = flask.request.args.get('postid')
    if get_error_code(postid):
        return flask.jsonify({}), get_error_code(postid)
    # username, has_error, error_code = check_authorization()

    # if has_error:
    #     return flask.jsonify({}), error_code

    # if postid_in_range(postid) is False:
    #     # if postid is not in range
    #     # return 404
    #     return flask.jsonify({}), 404

    if has_liked(username, postid):
        likeid = get_likeid(username, postid)
        context = {
            "likeid": likeid,
            "url": f"/api/v1/likes/{likeid}/"
            # "url": "/api/v1/likes/{}/".format(likeid)
        }
        return flask.jsonify(**context), 200

    connection = insta485.model.get_db()
    connection.execute(
        "INSERT INTO likes(owner, postid) "
        "VALUES (?, ?) ",
        (username, postid, )
    )
    connection.commit()
    likeid = get_likeid(username, postid)
    context = {
        "likeid": likeid,
        "url": f"/api/v1/likes/{likeid}/"
        # "url": "/api/v1/likes/{}/".format(likeid)
    }
    return flask.jsonify(**context), 201


@insta485.app.route('/api/v1/likes/<likeid>/', methods=["DELETE"])
def delete_like(likeid):
    """Delete like using api."""
    # Delete one “like”. Return 204 on success.
    # If the likeid does not exist, return 404.
    # If the user does not own the like, return 403.
    username, has_error, error_code = check_authorization()
    if has_error:
        # 403
        return flask.jsonify({}), error_code
    if likeid_exists(likeid) is False:
        return flask.jsonify({}), 404
    if own_like(username, likeid) is False:
        return flask.jsonify({}), 403
    connection = insta485.model.get_db()
    connection.execute(
        "DELETE FROM likes WHERE likeid = ? ",
        (likeid, )
    )
    connection.commit()
    return flask.jsonify({}), 204
