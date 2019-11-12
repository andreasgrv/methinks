import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Entry(db.Model):
    __tablename__ = 'entry'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(), nullable=False)
    date = db.Column(db.Date(), index=True, nullable=False)
    last_edited = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow)
    misc = db.Column(db.JSON, nullable=True)

    def __init__(self, **data):
        self.id = data.pop('id')
        self.text = data.pop('text')
        self.date = data.pop('date')
        self.misc = data

    def __repr__(self):
        return 'Entry: %r:\n%s' % (self.date, self.text)

    def as_dict(self):
        d = dict(id=self.id,
                 text=self.text,
                 date=self.date,
                 last_edited=self.last_edited,
                 misc=self.misc)
        return d
