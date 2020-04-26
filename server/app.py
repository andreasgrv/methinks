import os
import argparse
import datetime
from flask import Flask, request
from flask_migrate import Migrate
from methinks.db import db, Entry
from methinks.utils import str_to_date
from utils import response


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
def root():
    return ''


@app.route('/entries/<date>')
def get_entry(date):
    if date == 'latest':
        entry = Entry.query.order_by(Entry.date.desc()).first()
    else:
        d = Entry.string_to_date(date)
        entry = Entry.query.filter_by(date=d).first()
    entry = {} if not entry else entry.as_dict()
    return response(True, 'OK', data=entry)


@app.route('/entries/create', methods=['POST'])
def create_entry():
    try:
        data = dict(request.json)
        token = data.pop('token')
        text = data.pop('text')
        dt = data.pop('date')
        dt = str_to_date(dt)
        entry = Entry(text=text, date=dt.date(), **data)
        db.session.add(entry)
        db.session.commit()
        return response(True, 'OK', data=entry.as_dict())
    except Exception as e:
        return response(False, msg=repr(e))


@app.route('/entries/update', methods=['POST'])
def update_entry():
    try:
        data = dict(request.json)
        token = data.pop('token')
        text = data.pop('text')
        dt = data.pop('date')
        dt = str_to_date(dt)
        entry = Entry.query.filter_by(date=dt.date()).first()
        if entry is None:
            raise ValueError("Failed to update entry.")
        entry.text = text
        entry.misc = data
        entry.last_edited = datetime.datetime.now()
        print(entry)
        db.session.add(entry)
        db.session.commit()
        return response(True, 'OK', data=entry.as_dict())
    except Exception as e:
        return response(False, msg=repr(e))


@app.route('/entries/delete', methods=['POST'])
def delete_entry():
    try:
        dt = str_to_date(request.json['date'])
        entry = Entry.query.filter_by(date=dt.date()).first()
        if entry:
            db.session.delete(entry)
            db.session.commit()
        return response(True, 'OK')
    except Exception as e:
        return response(False, msg=repr(e))
    return response(200, 'OK')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run server')
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=8000, debug=True)
