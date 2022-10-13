import flask
import insta485
import hashlib

def check_authorization():
    # Every REST API route should return 403 if a user is not authenticated.
    # return username, has_error (True or Flase), error_code (403)
    if "username" in flask.session:
        # Authentication with session cookies should also work. 
        # This is true for every route with the exception of /api/v1/
        username = flask.session["username"]
        return username, False, None

    if flask.request.authorization:
        # HTTP Basic Access Authentication should work. 
        # This is true for every route with the exception of /api/v1/.
        username = flask.request.authorization['username'] 
        password = flask.request.authorization['password'] 
    else:
        return None, True, 403
    
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT username, password "
        "FROM users WHERE username= ? ",
        (username,)
    )
    result = cur.fetchone()
    if result:
        # check password for given username
        correct_password = result["password"]
        algorithm = 'sha512'
        salt = correct_password.split('$')[1]
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])
        if correct_password == password_db_string:
            flask.session["username"] = username
            return username, False, None
    return None, True, 403

def postid_in_range(postid):
    # Post IDs that are out of range should return a 404 error.
    # return True if postid is in range
    # return False if postid is not in range
    connection = insta485.model.get_db()
    cur = connection.execute(
            "SELECT * FROM posts WHERE postid = ? ",
            (postid, )
        )
    return len(cur.fetchall()) != 0

def commentid_in_range(commentid):
    # Post IDs that are out of range should return a 404 error.
    # return True if postid is in range
    # return False if postid is not in range
    connection = insta485.model.get_db()
    cur = connection.execute(
            "SELECT * FROM comments WHERE commentid = ? ",
            (commentid, )
        )
    return len(cur.fetchall()) != 0
