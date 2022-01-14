from dataclasses import dataclass
from sqlite3 import IntegrityError, Error
from typing import TypeVar, Type, Union

from werkzeug.security import generate_password_hash

from flaskr.db import get_db

U = TypeVar("U", bound="User")


@dataclass
class User:
    user_id: int
    username: str
    password: str

    @classmethod
    def load_from_username(cls: Type[U], username: str) -> Union[U, None]:
        query = """
            SELECT * FROM user WHERE username = ?;
        """
        if (user := get_db().execute(query, (username,)).fetchone()) is None:
            return None
        return cls(**user)

    @classmethod
    def load_from_id(cls: Type[U], user_id: str) -> Union[U, None]:
        query = """
            SELECT * FROM user WHERE user_id = ?;
        """
        if (user := get_db().execute(query, (user_id,)).fetchone()) is None:
            return None
        return cls(**user)

    @classmethod
    def create_user(cls: Type[U], username: str, password: str) -> U:
        query = """
            INSERT INTO user (username, password) VALUES (?, ?);
        """
        hashed_password = generate_password_hash(password)
        try:
            user_id = get_db().execute(query, (username, hashed_password)).lastrowid
        except IntegrityError as db_error:
            raise Error(f"{username} is already registered!") from db_error
        else:
            get_db().commit()
        return cls(user_id=user_id, username=username, password=hashed_password)
