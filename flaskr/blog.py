from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.models.post import Post

bp = Blueprint("blog", __name__)


def get_post(post_id, check_author=True):
    post = Post.load_post(post_id)

    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")

    if check_author and post["author_id"] != g.user.user_id:
        abort(403)

    return post


@bp.route("/")
def index():
    posts = Post.load_all_posts()
    return render_template("blog/index.html.jinja", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title or not body:
            error = "Title AND body are required"

        if error is None:
            Post.create_post(title, body, g.user.user_id)
            return redirect(url_for("blog.index"))

        flash(error)

    return render_template("blog/create.html.jinja")


@bp.route("/update/<int:post_id>", methods=("GET", "POST"))
@login_required
def update(post_id):
    pass
