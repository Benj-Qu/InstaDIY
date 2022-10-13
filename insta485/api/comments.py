"""REST API for comments."""
from crypt import methods
import flask
import insta485
from utils import check_authorization

@insta485.app.route("/api/v1/comments/", methods=["POST"])
def add_comment():
    postid = flask.Request.args.get("postid")
