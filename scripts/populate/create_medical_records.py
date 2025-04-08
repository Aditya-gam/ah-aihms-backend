# File: scripts/populate/create_medical_records.py
import random
from datetime import UTC, datetime

from dotenv import load_dotenv

from app import create_app
from app.models.medical_record import MedicalRecord
from app.models.user import User
from scripts.populate.utils import generate_hash, https_url

# ✅ Load environment variables before importing the app
load_dotenv()  # Must be called before create_app()

app = create_app()


def create_medical_records():
    with app.app_context():
        print("Creating medical records...")
        MedicalRecord.drop_collection()

        records = []
        patients = list(User.objects(role="patient"))
        doctors = list(User.objects(role="doctor"))

        for patient in patients:
            for _ in range(random.randint(1, 3)):
                uploaded_by = random.choice(doctors)
                record = MedicalRecord(
                    patient_id=patient,
                    uploaded_by=uploaded_by,
                    document_hash=generate_hash(),
                    record_type=random.choice(["report", "prescription", "imaging"]),
                    description="Auto-generated for testing",
                    upload_date=datetime.now(UTC),
                    file_url=https_url(),
                )
                records.append(record)

        MedicalRecord.objects.insert(records, load_bulk=False)
        print(f"✅ Created {len(records)} medical records.")


if __name__ == "__main__":
    create_medical_records()
