import functools

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

from flaskr.user import create_user

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if not username or not password:
            error = "A username and password are required"

        if error is not None:
            if not (error := create_user(username, password)):
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")
