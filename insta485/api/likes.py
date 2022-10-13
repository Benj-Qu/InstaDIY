"""REST API for likes."""
import flask
import insta485
from utils import check_authorization
from db_operations import *

@insta485.app.route('/api/v1/likes/?postid=<postid>', methods=["POST"])
def show_like(postid):
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
        
