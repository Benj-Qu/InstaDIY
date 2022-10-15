"""Database operations."""
import insta485


def has_liked(username, postid):
    """Return True if username has already liked this postid."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE owner = ? AND postid = ?",
        (username, postid)
    )
    return len(cur.fetchall()) != 0


def get_likeid(username, postid):
    """Get likeid."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT likeid "
        "FROM likes "
        "WHERE owner = ? AND postid = ?",
        (username, postid, )
    )
    results = cur.fetchone()
    return results["likeid"]


def likeid_exists(likeid):
    """Return True if likeid exists. Else return False."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE likeid = ?",
        (likeid, )
    )
    return len(cur.fetchall()) != 0


def own_like(username, likeid):
    """Return True if username own the like. Else return False."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE likeid = ?",
        (likeid, )
    )
    results = cur.fetchone()
    owner = results["owner"]
    return owner == username


def own_comment(username, commentid):
    """Return True if username own the like, else return False."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * "
        "FROM comments "
        "WHERE commentid = ?",
        (commentid, )
    )
    results = cur.fetchone()
    owner = results["owner"]
    return owner == username


def delete_comment_db(commentid):
    """Delete a comment by commentid."""
    connection = insta485.model.get_db()
    connection.execute(
        "DELETE FROM comments WHERE commentid = ? ",
        (commentid, )
    )
    connection.commit()
