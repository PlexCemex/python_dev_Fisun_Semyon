import os
from flask import Flask
from .db import get_db
from .db import close_db
from faker import Faker
import random


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
        # print(fake.text(1000)) 


        for i in range(1,11):
            db_authors.execute('INSERT INTO author (id,email,login) VALUES (?,?,?)',[i,fake.email(), fake.user_name()])
        db_authors.commit()
        
        db_authors_cursor=db_authors.cursor()
        blogs_and_owners = {}

        for i in range(1,101):
            owner_id = random.randint(1,10)
            db_authors_cursor.execute('INSERT INTO blog (owner_id, name, description) VALUES (?,?,?)',[owner_id,fake.sentence(), fake.paragraph()])
            blogs_and_owners[db_authors_cursor.lastrowid] = owner_id
        db_authors.commit()

        # for i in range(1,1001):


        print(blogs_and_owners)
        close_db(db_general)
        close_db(db_authors)

    return app
