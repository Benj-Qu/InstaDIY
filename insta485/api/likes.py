"""REST API for likes."""
import flask
import insta485
from insta485.api import posts
from utils import check_authorization

@insta485.app.route('/api/v1/likes/?postid=<postid>', methods=["POST"])
def show_like(postid):
    connection = insta485.model.get_db()
    username, has_error, error_code = check_authorization()
    if has_error:
        return flask.jsonify({}), error_code
    


    
    # likeid = 

    # context = {
    #     "likeid": likeid,
    #     "url": f"/api/v1/likes/{likeid}/"
    # }
    # return flask.jsonify(**context), 201
