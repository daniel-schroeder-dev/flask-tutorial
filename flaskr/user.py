from werkzeug.security import generate_password_hash

from flaskr.db import get_db


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    @property
    def db(self):
        return get_db()

    @classmethod
    def load_from_username(cls, username):
        query = """
            SELECT * FROM user WHERE username = ?;
        """
        if (user := cls.db.execute(query, (username,)).fetchone()) is None:
            return None
        return cls(**user)

    @classmethod
    def load_from_id(cls, user_id):
        query = """
            SELECT * FROM user WHERE id = ?;
        """
        if (user := cls.db.execute(query, (user_id,)).fetchone()) is None:
            return None
        return cls(**user)

    @classmethod
    def create_user(cls, username, password):
        query = """
            INSERT INTO user (username, password) VALUES (?, ?);
        """
        try:
            hashed_password = generate_password_hash(password)
            user_id = cls.db.execute(query, (username, hashed_password)).lastrowid
            cls.db.commit()
            return cls(user_id, username, hashed_password)
        except cls.db.IntegrityError:
            raise Exception(f"{username} is already registered!")

    def __repr__(self):
        return f"<User username={self.username} id={self.id}>"
