import os
from flask import Flask
from .db import get_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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
        db = get_db(app)
        print("succes")
        with app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))

    return app
