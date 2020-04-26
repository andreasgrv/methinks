import os
from flask import Flask
from flask_migrate import Migrate

from methinks.db import db
from app.methinks import methinks_routes


db_uri = 'postgresql://%s:%s@localhost/%s' % (os.environ['METHINKS_DB_USER'],
                                              os.environ['METHINKS_DB_PASSWD'],
                                              os.environ['METHINKS_DB_NAME'])


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True

    app.register_blueprint(methinks_routes, url_prefix='/methinks')

    db.init_app(app)
    migrate = Migrate(app, db)
    # global options
    return app


app = create_app()
