# tests/conftest.py

import mongomock
import pytest
from mongoengine import connect, disconnect

from app import create_app


@pytest.fixture(scope="session")
def app():
    """
    Creates a Flask application instance for testing.
    This fixture has a session scope, so it's created once per test session.
    """
    test_app = create_app()
    test_app.config["TESTING"] = True
    return test_app


@pytest.fixture(scope="session")
def db():
    """
    Creates an in-memory MongoDB database using mongomock (new approach).
    The database is disconnected after all tests complete.
    """
    # Instead of using host="mongomock://localhost",
    # we specify the 'mongo_client_class=mongomock.MongoClient'
    # which is now the supported approach in modern MongoEngine.
    connect(
        db="testdb",
        alias="testdb_alias",
        mongo_client_class=mongomock.MongoClient,
    )

    yield  # Allow tests to run

    # Disconnect that specific alias after tests
    disconnect(alias="testdb_alias")


@pytest.fixture
def client(app, db):
    """
    Provides a Flask test client for sending requests to the application.
    Ensures each test runs in an isolated mongomock database context.
    """
    with app.test_client() as test_client:
        yield test_client
