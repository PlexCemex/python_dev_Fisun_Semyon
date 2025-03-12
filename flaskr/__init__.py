import os
from flask import Flask
from .db import get_db
from .db import close_db
from faker import Faker
import random
import datetime

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
        SECRET_KEY='dev',
        DATABASE_GENERAL=os.path.join(app.instance_path, 'general.sqlite'),
        DATABASE_AUTHORS=os.path.join(app.instance_path, 'authors.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    @app.route('/api/comments')
    def api_comments():
        return {
        "username": "user.username",
        "theme": "user.theme",
        "image": "url_for(user_image, filename=user.image)",
    }

    @app.route('/api/general')
    def api_general():
        return {
        "username": "user.username111",
        "theme": "user.theme11111",
        "image": "url_for(user_image, filename=user.image)11111",
    }

    @app.cli.command("init-db")
    def init_db_command():
        db_general, db_authors = get_db(app)

        with app.open_resource('./schema/general.sql') as f:
            db_general.executescript(f.read().decode('utf8'))

        with app.open_resource('./schema/authors.sql') as f:
            db_authors.executescript(f.read().decode('utf8'))

        fake = Faker()

        num_of_users = 10
        num_of_blogs = 50
        num_of_posts = 100
        num_of_comment = 500

        # Р В Р ВµР С–Р С‘РЎРѓРЎвЂљРЎР‚Р В°РЎвЂ Р С‘РЎРЏ РЎвЂћР ВµР в„–Р С”Р С•Р Р†РЎвЂ№РЎвЂ¦ Р С—Р С•Р В»РЎРЉР В·Р С•Р Р†Р В°РЎвЂљР ВµР В»Р ВµР в„–
        for i in range(1, num_of_users + 1):
            db_authors.execute('INSERT INTO author (id,email,login) VALUES (?,?,?)', [i, fake.email(), fake.user_name() ])
            db_general.execute('INSERT INTO logs (datetime, user_id, space_type_id, event_type_id) VALUES (?, ?, ?, ?)',
                               [   datetime.datetime(2020, i, 15), i, SPACE_TYPE_GLOBAL, EVENT_TYPE_LOGIN ])
        db_authors.commit()
        db_general.commit()

        db_authors_cursor = db_authors.cursor()
        blogs_and_owners = {}

        # Р В Р ВµР С–Р С‘РЎРѓРЎвЂљРЎР‚Р В°РЎвЂ Р С‘РЎРЏ Р В±Р В»Р С•Р С–Р С•Р Р† РЎР‹Р В·Р ВµРЎР‚Р С•Р Р†, РЎРѓР С•РЎвЂ¦РЎР‚Р В°Р Р…РЎРЏР ВµР С� РЎРѓР Р†РЎРЏР В·РЎРЉ Р В±Р В»Р С•Р С–Р В° Р С‘ РЎР‹Р В·Р ВµРЎР‚Р В° Р Р† blogs_and_owners
        for _ in range(1, num_of_blogs + 1):
            # Р вЂ�Р В»Р С•Р С–
            owner_id = random.randint(1,num_of_users)
            db_authors_cursor.execute('INSERT INTO blog (owner_id, name, description) VALUES (?,?,?)',[owner_id,fake.sentence(), fake.paragraph()])
            blogs_and_owners[db_authors_cursor.lastrowid] = owner_id
        db_authors.commit()

        for i in range(1,num_of_posts+1):
            blog_id = random.randint(1, num_of_blogs)
            db_authors_cursor.execute('INSERT INTO post (header, text, author_id, blog_id) VALUES (?,?,?,?)',
                                      [fake.sentence(), fake.text(500), blogs_and_owners[blog_id], blog_id] )
            
            # Р вЂєР С•Р С– Р С—РЎР‚Р С• Р В±Р В»Р С•Р С–
            db_general.execute('INSERT INTO logs (datetime, user_id, space_type_id, event_type_id) VALUES (?, ?, ?, ?)',
                               [   datetime.datetime(2021, 1, 1) + datetime.timedelta(days=i) , blogs_and_owners[blog_id], SPACE_TYPE_BLOG, EVENT_TYPE_CREATE_POST ])
        db_authors.commit()
        db_general.commit()

        for i in range (1,num_of_comment+1):
            owner_id = random.randint(1,num_of_users)
            db_general.execute('INSERT INTO logs (datetime, user_id, space_type_id, event_type_id) VALUES (?, ?, ?, ?)',
                               [   datetime.datetime(2021, 10, 1) + datetime.timedelta(hours=i) , owner_id, SPACE_TYPE_POST, EVENT_TYPE_COMMENT ])
        db_general.commit()
        
        close_db(db_general)
        close_db(db_authors)

    return app
