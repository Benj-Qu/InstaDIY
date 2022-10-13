import insta485

def has_liked(username, postid):
    """
    Return True if username has already liked this postid
    else return False
    """
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
    """
    Return True if likeid exists
    else return False
    """
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE likeid = ?",
        (likeid)
    )
    return len(cur.fetchall()) != 0


def own_like(username, likeid):
    """
    Return True if username own the like
    else return False
    """
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * "
        "FROM likes "
        "WHERE likeid = ?",
        (likeid)
    )
    results = cur.fetchone()
    owner = results["owner"]
    return owner == username
