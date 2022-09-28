"""Discription.

Utility functions.

"""

import uuid
import pathlib
from functools import wraps
import flask
import insta485
# import hashlib


def require_login(is_redirect=True):
    """Whether need to login."""
    def require_login_inner(func):
        """Inner function."""
        @wraps(func)
        def protected_endpoint(*args, **kws):
            """Protect endpoint."""
            if 'username' not in flask.session:
                if is_redirect:
                    return flask.redirect(flask.url_for("login"))
                flask.abort(403)
            return func(*args, **kws)
        return protected_endpoint
    return require_login_inner

# def require_login(f):
#     @wraps(f)
#     def protected_endpoint(*args, **kws):
#         if 'username' not in flask.session:
#             return flask.redirect(flask.url_for("login"))
#         return f(*args, **kws)
#     return protected_endpoint


# def require_login_403(f):
#     @wraps(f)
#     def protected_endpoint(*args, **kws):
#         if 'username' not in flask.session:
#             return flask.abort(403)
#         return f(*args, **kws)
#     return protected_endpoint


def uuid_file():
    """Send file to database and return uuid."""
    # Unpack flask object
    fileobj = flask.request.files["file"]
    filename = fileobj.filename

    if filename == '':
        return filename

    # Compute base name (filename without directory).  We use a UUID to avoid
    # clashes with existing files, and ensure that
    # the name is compatible with the
    # filesystem.
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix
    uuid_basename = f"{stem}{suffix}"
    # Save to disk
    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    return uuid_basename
