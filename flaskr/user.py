from werkzeug.security import generate_password_hash

from flaskr.db import get_db


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def load_from_username(cls, username):
        db = get_db()
        query = """
            SELECT * FROM user WHERE username = ?;
        """
        if (user := db.execute(query, (username,)).fetchone()) is None:
            return None
        return cls(**user)

    @classmethod
    def load_from_id(cls, user_id):
        db = get_db()
        query = """
            SELECT * FROM user WHERE id = ?;
        """
        if (user := db.execute(query, (user_id,)).fetchone()) is None:
            return None
        return cls(**user)

    @classmethod
    def create_user(cls, username, password):
        db = get_db()
        query = """
            INSERT INTO user (username, password) VALUES (?, ?);
        """
        try:
            hashed_password = generate_password_hash(password)
            user_id = db.execute(query, (username, hashed_password)).lastrowid
            db.commit()
            return cls(user_id, username, hashed_password)
        except db.IntegrityError:
            raise Exception(f"{username} is already registered!")

    def __repr__(self):
        return f"<User username={self.username} id={self.id}>"
