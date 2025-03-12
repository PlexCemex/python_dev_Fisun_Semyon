import sqlite3
from datetime import datetime

import click
from flask import current_app, g


def get_db(app):
    db_general = sqlite3.connect(
        app.config["DATABASE_GENERAL"], detect_types=sqlite3.PARSE_DECLTYPES
    )
    db_general.row_factory = sqlite3.Row

    db_authors = sqlite3.connect(
        app.config["DATABASE_AUTHORS"], detect_types=sqlite3.PARSE_DECLTYPES
    )
    db_authors.row_factory = sqlite3.Row

    return db_general, db_authors


def close_db(db):
    db.close()
