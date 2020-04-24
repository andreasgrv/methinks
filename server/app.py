import os
import argparse
from flask import Flask, request, render_template, render_template_string
from flask_migrate import Migrate
from methinks.db import db


db_uri = 'postgresql://%s:%s@localhost/%s' % (os.environ['DB_USER'],
                                              os.environ['DB_PASSWD'],
                                              os.environ['DB_NAME'])


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True

    db.init_app(app)
    migrate = Migrate(app, db)
    # global options
    return app


app = create_app()


@app.route('/')
def homepage():
    return 'hii'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run server')
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=8000, debug=True)
