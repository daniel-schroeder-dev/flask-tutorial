from typing import Union, TypeVar, Type, List

from flaskr.db import get_db
from dataclasses import dataclass

P = TypeVar("P", bound="Post")


@dataclass
class Post:
    post_id: int
    author_id: int
    title: str
    body: str
    created_at: str
    username: str

    @classmethod
    def load_post(cls: Type[P], post_id: int) -> Union[P, None]:
        query = """
            SELECT 
                post.post_id, post.title, post.body, post.author_id, 
                strftime("%Y-%m-%d", post.created_at) AS created_at,
                user.username
            FROM post
            JOIN user
            ON post.author_id = user.user_id
            WHERE post.post_id = ?;
        """
        if (post := get_db().execute(query, (post_id,)).fetchone()) is None:
            return None
        return cls(**post)

    @classmethod
    def create_post(cls: Type[P], title: str, body: str, user_id: int):
        query = """
            INSERT INTO post (title, body, author_id)
            VALUES (?, ?, ?);
        """
        get_db().execute(query, (title, body, user_id))
        get_db().commit()

    @classmethod
    def load_all_posts(cls: Type[P]) -> List[P]:
        query = """
            SELECT 
                post.post_id, post.title, post.body, post.author_id,
                strftime("%Y-%m-%d", post.created_at) AS created_at, 
                user.username
            FROM post
            JOIN user
            ON post.author_id = user.user_id
            ORDER BY created_at DESC;
        """
        return [cls(**post) for post in get_db().execute(query).fetchall()]

    @classmethod
    def update_post(cls: Type[P], post_id: int, title: str, body: str):
        query = """
            UPDATE post
            SET title = ?, body = ?
            WHERE post_id = ?;
        """
        get_db().execute(query, (title, body, post_id))
        get_db().commit()
