import os
import datetime
import xxhash
import json
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Entry(db.Model):
    __tablename__ = 'entry'

    DATEFORMAT = '%Y-%m-%d-%a'

    id = db.Column(db.Integer, primary_key=True)
    hexid = db.Column(db.String(16), unique=True, nullable=False, index=True)
    text = db.Column(db.Text(), nullable=False)
    date = db.Column(db.Date(), index=True, nullable=False)
    last_edited = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    misc = db.Column(db.JSON, nullable=True)

    def __init__(self, **data):
        if 'id' in data:
            raise AttributeError('id cannot be set')
        if 'hexid' in data:
            raise AttributeError('hexid cannot be set')
        self.text = data.pop('text')
        self.date = data.pop('date')
        assert type(self.date) is datetime.date
        self.misc = data

        self.hexid = self.hash

    def __repr__(self):
        return 'Entry: %r:\n%s' % (self.date, self.text)

    @property
    def hash(self):
        content = '%s%s%s' % (self.text, self.date, json.dumps(self.misc))
        hs = xxhash.xxh64(content).hexdigest()
        return hs

    @classmethod
    def string_to_date(cl, text):
        return datetime.datetime.strptime(text, cl.DATEFORMAT).date()

    @classmethod
    def date_to_string(cl, date):
        return date.strftime(cl.DATEFORMAT)

    @property
    def filename(self):
        return '%s.md' % Entry.date_to_string(self.date)

    def as_dict(self):
        d = dict(id=self.id,
                 hexid=self.hexid,
                 text=self.text,
                 date=self.date,
                 last_edited=self.last_edited,
                 misc=self.misc)
        return d

    def to_file(self, folderpath):
        path = os.path.join(folderpath, self.filename)
        with open(path, 'w') as f:
            f.write(self.text)

    @classmethod
    def from_file(cl, filepath):
        with open(filepath, 'r') as f:
            contents = f.read()
        filename = os.path.basename(filepath).replace('.md', '')
        date = cl.string_to_date(filename)
        return Entry(text=contents, date=date)
