import pytest
from mongoengine import ValidationError

from app.models.analytics_data import AnalyticsData
from app.models.user import EmergencyContact, User


@pytest.fixture
def patient(db):
    """
    Creates a simple patient user fixture
    """
    patient = User(
        email="analytics_patient@example.com",
        password_hash="patient_pass",
        role="patient",
        first_name="Analytics",
        last_name="Test",
        phone_number="1112223333",
        address="Some address",
        emergency_contact=EmergencyContact(
            name="EC Name", relationship="Parent", phone_number="9999999999"
        ),
    ).save()
    return patient


def test_valid_analytics_data(db, patient):
    analytics = AnalyticsData(
        patient_id=patient,
        metrics={"heart_rate": 72, "blood_pressure": "120/80", "glucose_level": 90},
        prediction_results={"risk_of_diabetes": 0.05},
        generated_by_model="AI_Model_V1",
    )
    analytics.save()
    assert analytics.id is not None
    assert analytics.metrics["heart_rate"] == 72


def test_missing_mandatory_metric(db, patient):
    """
    'metrics' must include heart_rate, blood_pressure, and glucose_level
    """
    analytics = AnalyticsData(
        patient_id=patient,
        metrics={
            "heart_rate": 80,
            # 'blood_pressure' is missing
            "glucose_level": 95,
        },
        prediction_results={"risk_of_diabetes": 0.1},
        generated_by_model="AI_Model_V2",
    )
    with pytest.raises(ValidationError, match="Missing essential health metrics"):
        analytics.save()


def test_empty_prediction_results(db, patient):
    analytics = AnalyticsData(
        patient_id=patient,
        metrics={"heart_rate": 70, "blood_pressure": "110/70", "glucose_level": 100},
        prediction_results={},  # empty
        generated_by_model="AI_Model_V2",
    )
    with pytest.raises(ValidationError, match="At least one predictive result"):
        analytics.save()
