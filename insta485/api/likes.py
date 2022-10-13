"""REST API for likes."""
import flask
import insta485
from insta485.api.utils import check_authorization
from insta485.api.db_operations import *

@insta485.app.route('/api/v1/likes/', methods=["POST"])
def create_like():
    postid = flask.request.args.get('postid')
    username, has_error, error_code = check_authorization()
    if has_error:
        return flask.jsonify({}), error_code

    if has_liked(username, postid):
        likeid = get_likeid(username, postid)
        context = {
            "likeid": likeid,
            "url": f"/api/v1/likes/{likeid}/"
        }
        return flask.jsonify(**context), 200
    else:
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
        }
        return flask.jsonify(**context), 201


@insta485.app.route('/api/v1/likes/<likeid>/', methods=["DELETE"])
def delete_like(likeid):
    # Delete one “like”. Return 204 on success.
    # If the likeid does not exist, return 404.
    # If the user does not own the like, return 403.
    username, has_error, error_code = check_authorization()
    if has_error:
        return flask.jsonify({}), error_code
        
