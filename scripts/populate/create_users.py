# File: scripts/populate/create_users.py

"""
Creates fake users (doctors and patients) for the AH-AIHMS backend.

Features:
- 10 fake doctors and 50 patients
- Securely hashed passwords using bcrypt
- Realistic user details via Faker
- Randomized 2FA flags
- Mixed patient insurance and doctor-only fields
"""

import random

import bcrypt
from dotenv import load_dotenv

from app import create_app
from app.models.user import User
from scripts.populate.utils import (
    fake,
    generate_emergency_contact,
    generate_insurance_info,
)

# Load environment variables early
load_dotenv()


# Constants
NUM_PATIENTS = 200
NUM_DOCTORS = 20
DEFAULT_PASSWORD = "TestPassword123!"  # password used for all fake users

# Initialize Flask app context
app = create_app()


def create_users():
    """
    Seeds the database with fake users (doctors + patients),
    each with secure hashed passwords and complete profile details.
    """
    with app.app_context():
        print("🌱 Starting user creation...")

        # Optional: Drop existing users
        User.drop_collection()
        users = []

        for _ in range(NUM_DOCTORS):
            hashed = bcrypt.hashpw(DEFAULT_PASSWORD.encode("utf-8"), bcrypt.gensalt()).decode(
                "utf-8"
            )
            user = User(
                email=fake.unique.email(),
                password_hash=hashed,
                role="doctor",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number(),
                address=fake.address(),
                emergency_contact=generate_emergency_contact(),
                verified=True,
                two_factor_enabled=random.choice([True, False]),
            )
            users.append(user)

        for _ in range(NUM_PATIENTS):
            hashed = bcrypt.hashpw(DEFAULT_PASSWORD.encode("utf-8"), bcrypt.gensalt()).decode(
                "utf-8"
            )
            user = User(
                email=fake.unique.email(),
                password_hash=hashed,
                role="patient",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number(),
                address=fake.address(),
                emergency_contact=generate_emergency_contact(),
                insurance_info=generate_insurance_info(),
                verified=True,
                two_factor_enabled=random.choice([True, False]),
            )
            users.append(user)

        # Bulk insert users
        User.objects.insert(users, load_bulk=False)
        print(f"✅ Created {NUM_DOCTORS} doctors and {NUM_PATIENTS} patients.")
        print(f"🔐 Default password for all users: '{DEFAULT_PASSWORD}'")


if __name__ == "__main__":
    create_users()
