# File: scripts/populate/create_analytics_data.py
import random
from datetime import UTC, datetime

from dotenv import load_dotenv

from app import create_app
from app.models.analytics_data import AnalyticsData
from app.models.user import User

# ✅ Load environment variables before importing the app
load_dotenv()  # Must be called before create_app()

app = create_app()


def create_analytics():
    with app.app_context():
        print("Creating analytics data...")
        AnalyticsData.drop_collection()

        records = []
        patients = list(User.objects(role="patient"))

        for patient in patients:
            for _ in range(random.randint(1, 3)):
                record = AnalyticsData(
                    patient_id=patient,
                    metrics={
                        "heart_rate": random.randint(60, 100),
                        "blood_pressure": f"{random.randint(110, 140)}/{random.randint(70, 90)}",
                        "glucose_level": random.uniform(80, 120),
                    },
                    prediction_results={
                        "diabetes_risk": random.uniform(0, 1),
                        "heart_disease_risk": random.uniform(0, 1),
                    },
                    generated_by_model="AI-Model-v1.2",
                    generated_at=datetime.now(UTC),
                )
                records.append(record)

        AnalyticsData.objects.insert(records, load_bulk=False)
        print(f"✅ Created {len(records)} analytics records.")


if __name__ == "__main__":
    create_analytics()
