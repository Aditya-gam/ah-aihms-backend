# File: scripts/populate/utils.py
import hashlib
import random

from faker import Faker

fake = Faker()


def generate_emergency_contact():
    return {
        "name": fake.name(),
        "relationship": random.choice(["Parent", "Sibling", "Spouse", "Friend"]),
        "phone_number": fake.phone_number(),
    }


def generate_insurance_info():
    return {
        "provider": fake.company(),
        "policy_number": fake.bothify(text="POL-####-####"),
        "group_number": fake.bothify(text="GRP-###"),
        "effective_date": fake.date_time_between(start_date="-2y", end_date="now"),
        "expiration_date": fake.date_time_between(start_date="now", end_date="+2y"),
    }


def generate_hash():
    return hashlib.sha256(fake.uuid4().encode("utf-8")).hexdigest()


def https_url(path="records/record.pdf"):
    return f"https://storage.fakehealth.org/{fake.uuid4()}/{path}"
