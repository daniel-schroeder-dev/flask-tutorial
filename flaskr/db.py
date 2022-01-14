from sqlite3 import Connection, connect, PARSE_DECLTYPES, Row

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db() -> Connection:
    if "db" not in g:
        g.db = connect(
            current_app.config["DATABASE"],
            detect_types=PARSE_DECLTYPES,
        )
        g.db.row_factory = Row

    return g.db


def close_db(err=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


@click.command("rebuild-db")
# https://flask.palletsprojects.com/en/2.0.x/cli/#application-context
@with_appcontext
def rebuild_db():
    """Runs schema.sql to rebuild the db."""
    db = get_db()

    with current_app.open_resource("schema.sql", mode="rt") as sql_file:
        db.executescript(sql_file.read())

    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(rebuild_db)
