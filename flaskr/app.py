import os
from flask import Flask, abort
from .db import get_db
from .db import close_db
from faker import Faker
import random
import datetime
from flask import request

SPACE_TYPE_GLOBAL = 1
SPACE_TYPE_BLOG = 2
SPACE_TYPE_POST = 3

EVENT_TYPE_LOGIN = 1
EVENT_TYPE_LOGOUT = 2
EVENT_TYPE_CREATE_POST = 3
EVENT_TYPE_DELETE_POST = 4
EVENT_TYPE_COMMENT = 5 


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE_GENERAL=os.path.join(app.instance_path, "general.sqlite"),
        DATABASE_AUTHORS=os.path.join(app.instance_path, "authors.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # export comments api
    @app.route("/api/comments")
    def api_comments():
        login = request.args.get("login", "")
        if login == "":
            abort(404)

        db_general, db_authors = get_db(app)
        res = db_authors.execute(
            """
            SELECT a2.login AS login_of_commentor, c.post_id, COUNT(*) AS count_of_comments, p.header AS post_header, a.login AS login_of_authon_post
            FROM comment AS c
            JOIN post p on p.id = c.post_id
            JOIN author a on a.id = p.author_id
            JOIN author a2 on a2.id = c.author_id
            WHERE a2.login = ?
            GROUP BY c.post_id
            """,
            [login],
        )
        rows = res.fetchall()

        close_db(db_authors)

        json = []
        for z in rows:
            json.append(
                {
                    "login": z["login_of_commentor"],
                    "post_id": z["post_id"],
                    "count_of_comments": z["count_of_comments"],
                    "post_header": z["post_header"],
                    "login_of_authon_post": z["login_of_authon_post"],
                }
            )

        return json

    # export logs api
    @app.route("/api/general")
    def api_general():
        login = request.args.get("login", "")
        if login == "":
            abort(404)

        db_general, db_authors = get_db(app)
        row = db_authors.execute(
            """
            SELECT a.id
            FROM author AS a
            WHERE a.login = ?
        """,
            [login],
        ).fetchone()
        id = row['id']

        res = db_general.execute(
            """
            SELECT  DATE (l.datetime) AS date_of_events,
            (SELECT COUNT(*) FROM logs AS ll WHERE ll.user_id = l.user_id AND ll.event_type_id = 1 AND DATE (ll.datetime) = DATE (l.datetime)) AS count_of_logins,
            (SELECT COUNT(*) FROM logs AS ll WHERE ll.user_id = l.user_id AND ll.event_type_id = 2 AND DATE (ll.datetime) = DATE (l.datetime)) AS count_of_logouts,
            (SELECT COUNT(*) FROM logs AS ll WHERE ll.user_id = l.user_id AND ll.event_type_id IN (3,4) AND DATE (ll.datetime) = DATE (l.datetime)) AS count_of_blog_actions
            FROM logs AS l
            WHERE user_id= ?
            GROUP BY datetime
            """,
            [id],
        )
        rows = res.fetchall()
        close_db(db_authors)
        close_db(db_general)

        json = []
        for z in rows:
            json.append(
                { 
                    "date_of_events": z["date_of_events"],
                    "count_of_logins": z["count_of_logins"],
                    "count_of_logouts": z["count_of_logouts"],
                    "count_of_blog_actions": z["count_of_blog_actions"],
                }
            )

        return json

    # init database schema and fake data to work with it
    @app.cli.command("init-db")
    def init_db_command():
        db_general, db_authors = get_db(app)

        with app.open_resource("./schema/general.sql") as f:
            db_general.executescript(f.read().decode("utf8"))

        with app.open_resource("./schema/authors.sql") as f:
            db_authors.executescript(f.read().decode("utf8"))

        fake = Faker()

        num_of_users = 10
        num_of_blogs = 50
        num_of_posts = 100

        # generate fake users and their login activity
        for i in range(1, num_of_users + 1):
            db_authors.execute(
                "INSERT INTO author (id,email,login) VALUES (?,?,?)",
                [i, fake.email(), fake.user_name()],
            )
            db_general.execute(
                "INSERT INTO logs (datetime, user_id, space_type_id, event_type_id) VALUES (?, ?, ?, ?)",
                [
                    datetime.datetime(2020, i, 15),
                    i,
                    SPACE_TYPE_GLOBAL,
                    EVENT_TYPE_LOGIN,
                ],
            )
        db_authors.commit()
        db_general.commit()

        db_authors_cursor = db_authors.cursor()
        blogs_and_owners = {}

        # generate fake blogs
        for _ in range(1, num_of_blogs + 1):
            owner_id = random.randint(1, num_of_users)
            db_authors_cursor.execute(
                "INSERT INTO blog (owner_id, name, description) VALUES (?,?,?)",
                [owner_id, fake.sentence(), fake.paragraph()],
            )
            blogs_and_owners[db_authors_cursor.lastrowid] = owner_id
        db_authors.commit()

        # generate fake posts and may be comment for them
        for i in range(1, num_of_posts + 1):
            blog_id = random.randint(1, num_of_blogs)
            db_authors_cursor.execute(
                "INSERT INTO post (header, text, author_id, blog_id) VALUES (?,?,?,?)",
                [fake.sentence(), fake.text(500), blogs_and_owners[blog_id], blog_id],
            )

            db_general.execute(
                "INSERT INTO logs (datetime, user_id, space_type_id, event_type_id) VALUES (?, ?, ?, ?)",
                [
                    datetime.datetime(2021, 1, 1) + datetime.timedelta(days=i),
                    blogs_and_owners[blog_id],
                    SPACE_TYPE_BLOG,
                    EVENT_TYPE_CREATE_POST,
                ],
            )

            for _ in range(3):
                if random.random() < 0.5:
                    owner_id = random.randint(1, num_of_users)
                    db_authors_cursor.execute(
                        "INSERT INTO comment (text, author_id, post_id) VALUES (?, ?, ?)",
                        [fake.text(), owner_id, i],
                    )

                    db_general.execute(
                        "INSERT INTO logs (datetime, user_id, space_type_id, event_type_id) VALUES (?, ?, ?, ?)",
                        [
                            datetime.datetime(2021, 10, 1)
                            + datetime.timedelta(hours=i),
                            owner_id,
                            SPACE_TYPE_POST,
                            EVENT_TYPE_COMMENT,
                        ],
                    )

        db_authors.commit()
        db_general.commit()

        # save database
        close_db(db_general)
        close_db(db_authors)

    return app
