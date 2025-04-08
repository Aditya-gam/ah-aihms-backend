# File: scripts/populate/create_users.py
import random

from dotenv import load_dotenv

from app import create_app
from app.models.user import User
from scripts.populate.utils import (
    fake,
    generate_emergency_contact,
    generate_insurance_info,
)

load_dotenv()
app = create_app()

NUM_PATIENTS = 25
NUM_DOCTORS = 10


def create_users():
    with app.app_context():
        print("Creating users...")
        User.drop_collection()
        users = []

        for _ in range(NUM_DOCTORS):
            user = User(
                email=fake.unique.email(),
                password_hash="hashed-password-placeholder",
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
            user = User(
                email=fake.unique.email(),
                password_hash="hashed-password-placeholder",
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

        User.objects.insert(users, load_bulk=False)
        print(f"✅ Created {NUM_DOCTORS} doctors and {NUM_PATIENTS} patients.")


if __name__ == "__main__":
    create_users()
