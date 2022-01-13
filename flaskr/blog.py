from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("blog", __name__)


def get_post(post_id, check_author=True):
    db = get_db()
    query = """
        SELECT post.post_id, post.title, post.body, post.author_id, 
        strftime("%Y-%m-%d", post.created) as created,
        user.username
        FROM post
        JOIN user
        ON post.author_id = user.user_id
        WHERE post.post_id = ?;
    """
    post = db.execute(query, post_id).fetchone()

    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")
    
    if check_author and post["author_id"] != g.user.user_id:
        abort(403)

    return post


@bp.route("/")
def index():
    db = get_db()
    query = """
        SELECT 
            post.post_id, post.title, post.author_id, post.body,
            strftime("%Y-%m-%d", post.created) as created, 
            user.username
        FROM post
        JOIN user
        ON post.author_id = user.user_id
        ORDER BY created DESC;
    """
    posts = db.execute(query).fetchall()
    return render_template("blog/index.html.jinja", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title or not body:
            error = "Title AND body are required"
        
        if error is None:
            db = get_db()
            query = """
                INSERT INTO post (title, body, author_id)
                VALUES (?, ?, ?);
            """
            db.execute(query, (title, body, g.user.user_id))
            db.commit()
            return redirect(url_for("blog.index"))
        
        flash(error)

    return render_template("blog/create.html.jinja")



@bp.route("/update")
def update():
    pass