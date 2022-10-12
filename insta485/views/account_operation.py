"""Discription.

Insta485 account view.
URLs include:
/accounts/*

"""
import os
import uuid
import hashlib
import flask
import insta485
# import pathlib
# from insta485.config import UPLOAD_FOLDER
from insta485.views import util
# import arrow


@insta485.app.route('/accounts/login/', methods=["GET"])
def login():
    """Login page."""
    if "username" in flask.session:
        return flask.redirect(flask.url_for("show_index"))
    return flask.render_template("login.html")


@insta485.app.route('/accounts/logout/', methods=["POST"])
def logout():
    """Logout function."""
    if "username" in flask.session:
        flask.session.clear()
    return flask.redirect(flask.url_for("login"))


@insta485.app.route('/accounts/create/', methods=["GET"])
def create_account():
    """Create account."""
    if "username" in flask.session:
        return flask.redirect(flask.url_for("edit_account"))
    return flask.render_template("create.html")


@insta485.app.route('/accounts/delete/', methods=["GET"])
def delete_account():
    """Delete account."""
    context = {}
    context["logname"] = flask.session["username"]
    return flask.render_template("delete.html", **context)


@insta485.app.route('/accounts/edit/', methods=["GET"])
def edit_account():
    """Edit account."""
    context = {}
    context["logname"] = flask.session["username"]
    connection = insta485.model.get_db()
    context["fullname"] = (connection.execute(
        "SELECT fullname "
        "FROM users "
        "WHERE username = ? ",
        (context["logname"], )
    ).fetchone())["fullname"]
    context["email"] = (connection.execute(
        "SELECT email "
        "FROM users "
        "WHERE username = ? ",
        (context["logname"], )
    ).fetchone())["email"]
    context["user_img_url"] = (connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = ? ",
        (context["logname"], )
    ).fetchone())["filename"]
    return flask.render_template("edit.html", **context)


@insta485.app.route('/accounts/password/', methods=["GET"])
def password():
    """Password page."""
    context = {}
    context["logname"] = flask.session["username"]
    return flask.render_template("password.html", **context)


@insta485.app.route('/accounts/', methods=["POST"])
def account():
    """Account operation."""
    url = flask.request.args.get("target")
    if not url:
        url = flask.url_for("show_index")
    operation = flask.request.form["operation"]
    if operation == "login":
        op_login()
    elif operation == "create":
        op_create()
    elif operation == "delete":
        op_delete()
    elif operation == "edit_account":
        op_edit()
    elif operation == "update_password":
        op_update()
    return flask.redirect(url)


def op_login():
    """Login function."""
    usr = flask.request.form["username"]
    pwd = flask.request.form["password"]
    if usr is None or pwd is None:
        flask.abort(400)
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username = ? ",
        (usr, )
    )
    password_list = cur.fetchall()
    if len(password_list) == 0:
        flask.abort(403)
    algorithm = 'sha512'
    salt = password_list[0]["password"].split('$')[1]
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + pwd
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    if password_list[0]["password"] == password_db_string:
        flask.session["username"] = usr
        return
    flask.abort(403)


def op_create():
    """Create account function."""
    usr = flask.request.form["username"]
    pwd = flask.request.form["password"]
    fullname = flask.request.form["fullname"]
    email = flask.request.form["email"]
    file = util.uuid_file()

    if usr is None or pwd is None \
       or fullname is None or email is None:
        flask.abort(400)

    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT created "
        "FROM users "
        "WHERE username = ? ",
        (usr, )
    )
    if len(cur.fetchall()) > 0:
        flask.abort(409)

    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + pwd
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])

    cur = connection.execute(
        "INSERT INTO users "
        "(username, fullname, email, filename, password) "
        "VALUES (?, ?, ?, ?, ?) ",
        (usr, fullname, email, file, password_db_string, )
    )
    connection.commit()
    flask.session["username"] = usr


def op_delete():
    """Delete account function."""
    if "username" not in flask.session:
        flask.abort(403)
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT filename "
        "FROM posts "
        "WHERE owner = ? ",
        (flask.session["username"], )
    )
    posts = cur.fetchall()
    cur = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = ? ",
        (flask.session["username"], )
    )
    icons = cur.fetchall()
    cur = connection.execute(
        "DELETE FROM users "
        "WHERE username = ? ",
        (flask.session["username"], )
    )
    connection.commit()
    for post in posts:
        os.remove(str(insta485.app.config['UPLOAD_FOLDER'])
                  + "/" + post["filename"])
    for icon in icons:
        os.remove(str(insta485.app.config['UPLOAD_FOLDER'])
                  + "/" + icon["filename"])
    flask.session.clear()


def op_edit():
    """Edit account function."""
    if "username" not in flask.session:
        flask.abort(403)
    fullname = flask.request.form["fullname"]
    email = flask.request.form["email"]
    file = util.uuid_file()
    if fullname is None or email is None:
        flask.abort(400)
    connection = insta485.model.get_db()
    cur = connection.execute(
        "UPDATE users "
        "SET fullname = ?, email = ? "
        "WHERE username = ? ",
        (fullname, email, flask.session["username"], )
    )
    connection.commit()
    # print(file)
    if file != '':
        cur = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = ? ",
            (flask.session["username"], )
        )
        filename = cur.fetchall()[0]["filename"]
        os.remove(str(insta485.app.config['UPLOAD_FOLDER']) + "/" + filename)
        cur = connection.execute(
            "UPDATE users "
            "SET filename = ? "
            "WHERE username = ? ",
            (file, flask.session["username"], )
        )
        connection.commit()


def op_update():
    """Update account function."""
    if "username" not in flask.session:
        flask.abort(403)
    pwd = flask.request.form["password"]
    new_password1 = flask.request.form["new_password1"]
    new_password2 = flask.request.form["new_password2"]
    if pwd is None or new_password1 is None or new_password2 is None:
        flask.abort(400)
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username = ? ",
        (flask.session["username"], )
    )
    password_list = cur.fetchall()
    algorithm = 'sha512'
    # salt = uuid.uuid4().hex
    salt = password_list[0]["password"].split('$')[1]
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + pwd
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    if password_list[0]["password"] != password_db_string:
        flask.abort(403)
    if new_password1 != new_password2:
        flask.abort(401)

    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + new_password1
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])

    cur = connection.execute(
        "UPDATE users "
        "SET password = ? "
        "WHERE username = ? ",
        (password_db_string, flask.session["username"], )
    )
    connection.commit()
