"""REST API for likes."""
import flask
import insta485
from insta485.api import posts




@insta485.app.route('/api/v1/likes/?postid=<postid>', methods=["POST"])
def show_like(postid):
    likeid = 

    context = {
        "likeid": likeid,
        "url": f"/api/v1/likes/{likeid}/"
    }
    return flask.jsonify(**context), 201