from typing import List, Union

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.models.post import Post

bp = Blueprint("blog", __name__)


def get_post(post_id: int, check_author: bool = True) -> Post:
    post: Union[Post, None] = Post.load_post(post_id)

    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")

    if check_author and post.author_id != g.user.user_id:
        abort(403)

    return post


@bp.route("/")
def index():
    posts: List[Post] = Post.load_all_posts()
    return render_template("blog/index.html.jinja", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title: str = request.form["title"]
        body: str = request.form["body"]
        error: Union[str, None] = None

        if not title or not body:
            error = "Title AND body are required"

        if error is None:
            Post.create_post(title, body, g.user.user_id)
            return redirect(url_for("blog.index"))

        flash(error)

    return render_template("blog/create.html.jinja")


@bp.route("/update/<int:post_id>", methods=("GET", "POST"))
@login_required
def update(post_id: int):
    post: Post = get_post(post_id)

    if request.method == "POST":
        title: str = request.form["title"]
        body: str = request.form["body"]
        error: Union[str, None] = None

        if not title or not body:
            error = "Title and body text required!"

        if error is None:
            Post.update_post(post_id, title, body)
            return redirect(url_for("blog.index"))

        flash(error)

    return render_template("blog/update.html.jinja", post=post)


@bp.route("/delete/<int:post_id>", methods=("DELETE",))
@login_required
def delete(post_id: int):
    # Only calling this to show aborts if post is invalid
    get_post(post_id)
    Post.delete_post(post_id)
    return redirect(url_for("blog.index"))
