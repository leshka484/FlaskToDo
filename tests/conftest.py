import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash

from app.app import app as flask_app
from app.extensions import Base
from app.extensions import Session as AppSession
from app.models import User


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()
    db = scoped_session(sessionmaker(bind=connection))

    # Подменяем глобальную Session на тестовую
    AppSession.remove()
    AppSession.configure(bind=connection)

    yield db

    db.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def app():
    flask_app.config.update(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,
        }
    )
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def test_user(db_session):
    user = User(name="testuser", hashed_password=generate_password_hash("testpswrd"))
    db_session.add(user)
    db_session.commit()
    return user 