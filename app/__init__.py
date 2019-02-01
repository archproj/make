
import os
from config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app(server):
    app = Flask(__name__)

    app.config.from_object(config[server] or 'default') 
    config[server].init_app(app)


    try:
        dbpass = os.environ['DBPASS']
    except KeyError:
        # dev db does not have password
        dbpass = ''

    app.config.update(
        SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
            os.environ['DBUSER'],
            dbpass,
            os.environ['DBHOST'],
            os.environ['DBNAME']
        )
    )

    db.init_app(app)


    from .listen import listen as listen_blueprint
    app.register_blueprint(listen_blueprint, url_prefix='/listen')


    return app
