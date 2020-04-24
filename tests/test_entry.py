import pytest
import datetime
from methinks.db import Entry


now = datetime.date.today()


def test_hash_same():
    e1 = Entry(text='abra', date=now, misc=dict(a=3))
    e2 = Entry(text='abra', date=now, misc=dict(a=3))
    assert e1.hash == e2.hash


def test_hash_diff_times():
    e1 = Entry(text='abra', date=datetime.date.today(), misc=dict(a=3))
    e2 = Entry(text='abra', date=datetime.date.today() + datetime.timedelta(days=1), misc=dict(a=3))
    assert e1.hash != e2.hash


def test_hash_id_insensitive():
    e1 = Entry(text='abra', date=now)
    e2 = Entry(text='abra', date=now)
    assert e1.hash == e2.hash


def test_hash_misc_sensitive():
    e1 = Entry(text='abra', date=now, misc=dict(a=3))
    e2 = Entry(text='abra', date=now, misc=dict(a=4))
    assert e1.hash != e2.hash


def test_datetime_fails():
    with pytest.raises(AssertionError):
        e1 = Entry(text='abra', date=datetime.datetime.now(), misc=dict(a=3))


def test_file_serialization(tmp_path):
    e1 = Entry(text='abra', date=datetime.date.today())
    e1.to_file(tmp_path)
    fname = '%s.md' % Entry.date_to_string(e1.date)
    e2 = Entry.from_file(tmp_path / fname)
    assert e1.hash == e2.hash
