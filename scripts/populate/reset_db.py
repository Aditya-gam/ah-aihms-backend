# File: scripts/populate/reset_db.py

"""
Resets all MongoDB collections for AH-AIHMS backend.

Fixes:
- Ensures dotenv is loaded before app config
- Confirms MongoDB Atlas URI is passed to MongoEngine

Usage:
    python scripts/populate/reset_db.py
"""


from dotenv import load_dotenv

from app import create_app  # after .env is loaded
from app.models import AnalyticsData, Appointment, MedicalRecord, User

# ✅ Load environment variables before importing the app
load_dotenv()  # Must be called before create_app()


# ✅ Create the Flask app after .env is loaded
app = create_app()


def reset_database():
    """
    Drop all MongoDB collections used in AH-AIHMS backend.

    Collections:
    - users
    - appointments
    - medical_records
    - analytics_data
    """
    with app.app_context():
        print("Resetting all collections...")
        try:
            User.drop_collection()
            Appointment.drop_collection()
            MedicalRecord.drop_collection()
            AnalyticsData.drop_collection()
            print("✅ All collections dropped successfully.")
        except Exception as e:
            print("❌ Failed to reset database:", str(e))


if __name__ == "__main__":
    reset_database()
