from werkzeug.security import generate_password_hash

from flaskr.db import get_db


def get_user(username):
    pass


def create_user(username, password):
    db = get_db()
    query = """
        INSERT INTO user (username, password) VALUES (?, ?);
    """
    try:
        db.execute(query, (username, generate_password_hash(password)))
        db.commit()
    except db.IntegrityError:
        return f"{username} is already registered!"

    return None
