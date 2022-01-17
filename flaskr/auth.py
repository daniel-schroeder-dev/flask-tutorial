import functools
import sqlite3
from typing import Union

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from werkzeug.security import check_password_hash

from flaskr.models.user import User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.before_app_request
def load_logged_in_user():
    user_id: int = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = User.load_from_id(user_id)


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username: str = request.form["username"]
        password: str = request.form["password"]
        error: Union[str, None] = None

        if not username or not password:
            error = "A username and password are required"

        if error is None:
            try:
                User.create_user(username, password)
            except sqlite3.Error as err:
                error = err
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html.jinja")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username: str = request.form["username"]
        password: str = request.form["password"]
        error: Union[str, None] = None
        user: Union[User, None] = User.load_from_username(username)

        if user is None:
            error = "Invalid username!"
        elif not check_password_hash(user.password, password):
            error = "Invalid password!"

        if error is None:
            session.clear()
            session["user_id"] = user.user_id
            return redirect(url_for("blog.index"))

        flash(error)

    return render_template("auth/login.html.jinja")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("blog.index"))


def login_required(view_func):
    @functools.wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view_func(*args, **kwargs)

    return wrapped_view
