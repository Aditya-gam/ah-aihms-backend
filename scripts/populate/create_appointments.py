# File: scripts/populate/create_appointments.py
import random
from datetime import UTC, datetime, timedelta

from dotenv import load_dotenv

from app import create_app
from app.models.appointment import Appointment
from app.models.user import User

# ✅ Load environment variables before importing the app
load_dotenv()  # Must be called before create_app()

app = create_app()


def create_appointments():
    with app.app_context():
        print("Creating appointments...")
        Appointment.drop_collection()

        patients = list(User.objects(role="patient"))
        doctors = list(User.objects(role="doctor"))
        appointments = []

        for patient in patients:
            for _ in range(random.randint(2, 4)):
                doctor = random.choice(doctors)
                delta = timedelta(days=random.randint(-30, 30))
                time = datetime.now(UTC) + delta
                appointments.append(
                    Appointment(
                        patient_id=patient,
                        doctor_id=doctor,
                        appointment_time=time,
                        appointment_status=random.choice(["scheduled", "completed", "cancelled"]),
                        reason=random.choice(["Checkup", "Consultation", "Follow-up"]),
                    )
                )

        Appointment.objects.insert(appointments, load_bulk=False)
        print(f"✅ Created {len(appointments)} appointments.")


if __name__ == "__main__":
    create_appointments()
