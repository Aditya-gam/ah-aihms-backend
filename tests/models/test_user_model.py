import pytest
from mongoengine import NotUniqueError, ValidationError

from app.models.user import EmergencyContact, User


def test_create_valid_user(db):
    """
    GIVEN a valid User document data
    WHEN the user is saved to the DB
    THEN it should persist successfully without errors
    """
    user = User(
        email="test_user@example.com",
        password_hash="hashed_password",
        role="patient",
        first_name="Test",
        last_name="User",
        phone_number="1234567890",
        address="123 Main Street",
        emergency_contact=EmergencyContact(
            name="John Doe", relationship="Father", phone_number="9876543210"
        ),
    )
    user.save()
    assert user.id is not None
    assert user.role == "patient"
    assert user.verified is False
    assert user.created_at is not None
    assert user.updated_at is not None


def test_missing_required_field(db):
    """
    GIVEN a User document missing a required field (e.g., email)
    WHEN the user is saved
    THEN it should raise a ValidationError
    """
    user = User(
        password_hash="hashed_password",
        role="patient",
        first_name="Test",
        last_name="User",
        phone_number="1234567890",
        address="123 Main Street",
        emergency_contact=EmergencyContact(
            name="John Doe", relationship="Father", phone_number="9876543210"
        ),
    )
    with pytest.raises(ValidationError):
        user.save()


def test_unique_email_constraint(db):
    """
    GIVEN two User documents with the same email
    WHEN attempting to save the second user
    THEN a NotUniqueError should be raised
    """
    user1 = User(
        email="duplicate@example.com",
        password_hash="password123",
        role="patient",
        first_name="Jane",
        last_name="Doe",
        phone_number="1234567890",
        address="XYZ",
        emergency_contact=EmergencyContact(
            name="Someone", relationship="Brother", phone_number="5555555"
        ),
    )
    user1.save()

    user2 = User(
        email="duplicate@example.com",
        password_hash="another_password",
        role="doctor",
        first_name="Mike",
        last_name="Smith",
        phone_number="0987654321",
        address="ABC",
        emergency_contact=EmergencyContact(
            name="Another Person", relationship="Sister", phone_number="6666666"
        ),
    )
    with pytest.raises(NotUniqueError):
        user2.save()


def test_oauth_fields(db):
    """
    GIVEN a User document with optional OAuth fields
    WHEN the user is saved
    THEN it should persist if the (oauth_provider, oauth_id) pair is unique
    """
    user = User(
        email="oauth@example.com",
        password_hash="oauth_pass",
        role="patient",
        first_name="OAuth",
        last_name="Test",
        phone_number="1234567890",
        address="123 OAuth Lane",
        emergency_contact=EmergencyContact(
            name="Jane Roe", relationship="Sister", phone_number="1112223333"
        ),
        oauth_provider="google",
        oauth_id="google-unique-id",
    )
    user.save()
    assert user.id is not None


def test_insurance_info_optional(db):
    """
    GIVEN a User with no insurance info
    WHEN saved
    THEN it should persist with default None insurance info
    """
    user = User(
        email="test_insurance@example.com",
        password_hash="hashed_password",
        role="patient",
        first_name="No",
        last_name="Insurance",
        phone_number="1234567890",
        address="123 Unknown St",
        emergency_contact=EmergencyContact(
            name="Emergency Contact", relationship="Guardian", phone_number="9998887777"
        ),
    )
    user.save()
    assert user.insurance_info is None
