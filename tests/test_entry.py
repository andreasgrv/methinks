import datetime
from methinks.db import Entry


now = datetime.datetime.now()


def test_hash_same():
    e1 = Entry(id=0, text='abra', date=now, misc=dict(a=3))
    e2 = Entry(id=0, text='abra', date=now, misc=dict(a=3))
    assert e1.hash == e2.hash


def test_hash_diff_times():
    e1 = Entry(id=0, text='abra', date=datetime.datetime.now(), misc=dict(a=3))
    e2 = Entry(id=0, text='abra', date=datetime.datetime.now(), misc=dict(a=3))
    assert e1.hash != e2.hash


def test_hash_id_insensitive():
    e1 = Entry(id=0, text='abra', date=now)
    e2 = Entry(id=1, text='abra', date=now)
    assert e1.hash == e2.hash


def test_hash_misc_sensitive():
    e1 = Entry(id=0, text='abra', date=now, misc=dict(a=3))
    e2 = Entry(id=0, text='abra', date=now, misc=dict(a=4))
    assert e1.hash != e2.hash
