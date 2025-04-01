import datetime
from datetime import UTC

from mongoengine import DateTimeField  # ObjectIdField,
from mongoengine import (
    BooleanField,
    Document,
    EmailField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    EnumField,
    StringField,
)

# from app import db

# Nested document for Emergency Contact


class EmergencyContact(EmbeddedDocument):
    name = StringField(required=True, max_length=100)
    relationship = StringField(required=True, max_length=50)
    phone_number = StringField(required=True, max_length=20)


# Nested document for Insurance Information (can expand as needed)


class InsuranceInfo(EmbeddedDocument):
    provider = StringField(required=True, max_length=100)
    policy_number = StringField(required=True, max_length=50)
    group_number = StringField(max_length=50)
    effective_date = DateTimeField()
    expiration_date = DateTimeField()


class User(Document):
    meta = {
        "collection": "users",
        "indexes": [
            {"fields": ["email"], "unique": True},
            {"fields": ["role"]},
            {"fields": ["oauth_provider", "oauth_id"], "unique": True, "sparse": True},
        ],
    }

    # Basic user identification
    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True)

    # User role within the application
    role = EnumField(choices=["patient", "doctor", "admin"], required=True)

    # User profile details
    first_name = StringField(required=True, max_length=50)
    last_name = StringField(required=True, max_length=50)
    phone_number = StringField(required=True, max_length=20)
    address = StringField(required=True, max_length=255)

    # Additional user information
    emergency_contact = EmbeddedDocumentField(EmergencyContact, required=True)
    insurance_info = EmbeddedDocumentField(InsuranceInfo, required=False)

    # Security and verification fields
    verified = BooleanField(default=False)  # Email verification
    two_factor_enabled = BooleanField(default=False)

    # OAuth integration (optional)
    oauth_provider = EnumField(choices=["google", "apple"], required=False)
    oauth_id = StringField(required=False)

    # Automatic timestamps
    created_at = DateTimeField(default=lambda: datetime.datetime.now(UTC))
    updated_at = DateTimeField(default=lambda: datetime.datetime.now(UTC))

    def clean(self):
        """Automatically updates the 'updated_at' timestamp on every save operation"""
        self.updated_at = datetime.datetime.now(UTC)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
