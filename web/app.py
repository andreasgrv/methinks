import os
import argparse
from flask import Flask, request, render_template, render_template_string
from flask_migrate import Migrate
from methinks.db import db

# create our application :)
app = Flask(__name__)

# global options
app.config['DEBUG'] = True

db_uri = 'postgres://%s:%s@localhost/%s' % (os.environ['DB_USER'],
                                            os.environ['DB_PASSWD'],
                                            os.environ['DB_NAME'])
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def homepage():
    return 'hii'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run server')
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=8000, debug=True)
