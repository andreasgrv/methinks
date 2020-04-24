import datetime
from methinks.db import Entry
import pytest
from server.app import create_app
from server.app import db as _db
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="session")
def app(request):
    """
    Returns session-wide application.
    """
    return create_app()


@pytest.fixture(scope="session")
def db(app, request):
    """
    Returns session-wide initialised database.
    """
    with app.app_context():
        _db.drop_all()
        _db.create_all()


@pytest.fixture(scope="function", autouse=True)
def session(app, db, request):
    """
    Returns function-scoped session.
    """
    with app.app_context():
        conn = _db.engine.connect()
        txn = conn.begin()

        options = dict(bind=conn, binds={})
        sess = _db.create_scoped_session(options=options)

        # establish  a SAVEPOINT just before beginning the test
        # (http://docs.sqlalchemy.org/en/latest/orm/session_transaction.html#using-savepoint)
        sess.begin_nested()

        @event.listens_for(sess(), 'after_transaction_end')
        def restart_savepoint(sess2, trans):
            # Detecting whether this is indeed the nested transaction of the test
            if trans.nested and not trans._parent.nested:
                # The test should have normally called session.commit(),
                # but to be safe we explicitly expire the session
                sess2.expire_all()
                sess.begin_nested()

        _db.session = sess
        yield sess

        # Cleanup
        sess.remove()
        # This instruction rollsback any commit that were executed in the tests.
        txn.rollback()
        conn.close()


def test_insert(session):
    e = Entry(text='My example', date=datetime.date.today())
    session.add(e)
    session.commit()


def test_delete(session):
    e = Entry(text='My example', date=datetime.date.today())
    session.add(e)
    session.commit()
    session.delete(e)
    session.commit()


def test_find_by_hash(session):
    e = Entry(text='My example', date=datetime.date.today())
    session.add(e)
    session.commit()
    first = Entry.query.filter(Entry.hexid == e.hash).first()
    assert first == e
