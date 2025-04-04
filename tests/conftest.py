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


# <-- Use function scope instead of session scope
@pytest.fixture(scope="function")
def db():
    """
    Creates a brand-new in-memory MongoDB database using mongomock for each test.
    This prevents duplicate key errors when creating the same user in multiple tests.
    """
    connect(
        db="testdb",
        alias="default",  # Use 'default' to match the models' default alias
        mongo_client_class=mongomock.MongoClient,
    )

    yield  # Run the actual test

    # Disconnect so the next test starts from a blank DB
    disconnect(alias="default")


@pytest.fixture
def client(app, db):
    """
    Provides a Flask test client for sending requests to the application.
    Uses the function-scoped in-memory DB. Each test is isolated.
    """
    with app.test_client() as test_client:
        yield test_client
