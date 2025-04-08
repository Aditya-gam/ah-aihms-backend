# File: tests/conftest.py
"""
Test Configuration and Fixture Setup

This module sets up the core fixtures for our Flask application tests:
  - app: Creates a Flask application instance configured for testing.
  - db: Sets up an in-memory MongoDB database via mongomock for test isolation.
  - client: Provides a Flask test client for sending HTTP requests.
  - verified_doctor: Factory fixture for a verified doctor user (for testing doctor-specific flows).
  - (Additional factory fixtures such as verified_patient can be added similarly.)
"""

import mongomock
import pytest
from mongoengine import connect, connection, disconnect

from app import create_app

# Import the User model and related classes for use in factory fixtures.
from app.models.user import EmergencyContact, User


@pytest.fixture(scope="session")
def app():
    """
    Creates and returns a Flask application instance configured for testing.

    The application configuration is loaded from app.config.Config,
    and the TESTING flag is set to True to enable error propagation and disable exception catching.

    Returns:
        Flask: A Flask application instance.
    """
    test_app = create_app()
    test_app.config["TESTING"] = True
    return test_app


@pytest.fixture(scope="function")
def db():
    """
    Sets up a brand-new in-memory MongoDB database using mongomock for every test function.

    This fixture ensures each test has an isolated database environment,
    preventing collisions with the global (default) connection created by the application.

    Yields:
        None: The database connection is available in the background.

    Finally, the MongoDB connection is disconnected to start fresh for the next test.
    """
    # Disconnect existing connection if registered to avoid conflicts.
    if "default" in connection._connections:
        disconnect(alias="default")

    # Establish a new connection using mongomock with 'standard' UUID representation.
    connect(
        db="testdb",
        alias="default",
        mongo_client_class=mongomock.MongoClient,
        uuidRepresentation="standard",  # Resolves DeprecationWarning in MongoEngine
    )
    yield
    disconnect(alias="default")


@pytest.fixture
def client(app, db):
    """
    Provides a Flask test client for sending HTTP requests to the application.

    This fixture uses the function-scoped in-memory database provided by db() and
    ensures each test uses an isolated test client instance.

    Yields:
        FlaskClient: The test client for performing API calls in tests.
    """
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def verified_doctor(db):
    """
    Creates and returns a verified doctor user for testing doctor-specific functionalities.

    This fixture sets up a user document representing a verified doctor with all necessary fields.
    The returned user instance can be used in tests that require a doctor with specific attributes.

    Returns:
        User: A verified doctor user document saved in the in-memory test database.
    """
    doctor = User(
        email="doctor_verified@example.com",
        # In a real scenario, use bcrypt.hashpw to generate a proper hash.
        password_hash="hashed_doctor_password",
        role="doctor",
        first_name="Verified",
        last_name="Doctor",
        phone_number="5551112222",
        address="Dr. Street",
        emergency_contact=EmergencyContact(
            name="Doc Contact", relationship="Family", phone_number="4445556666"
        ),
        verified=True,
    )
    doctor.save()
    return doctor


# Optionally, you can add more fixtures such as a verified patient fixture:
#
# @pytest.fixture
# def verified_patient(db):
#     patient = User(
#         email="patient_verified@example.com",
#         password_hash="hashed_patient_password",
#         role="patient",
#         first_name="Verified",
#         last_name="Patient",
#         phone_number="5553334444",
#         address="Patient Ave",
#         emergency_contact=EmergencyContact(
#             name="Patient Contact", relationship="Friend", phone_number="7778889999"
#         ),
#         verified=True,
#     )
#     patient.save()
#     return patient
