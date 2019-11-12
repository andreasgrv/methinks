import datetime
import xxhash
import json
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Entry(db.Model):
    __tablename__ = 'entry'

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

    def as_dict(self):
        d = dict(id=self.id,
                 hexid=self.hexid,
                 text=self.text,
                 date=self.date,
                 last_edited=self.last_edited,
                 misc=self.misc)
        return d
