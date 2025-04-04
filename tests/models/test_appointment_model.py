from datetime import UTC, datetime

import pytest
from mongoengine import ValidationError

from app.models import Appointment, User
from app.models.user import EmergencyContact


@pytest.fixture
def doctor_and_patient(db):
    """
    Creates a doctor user and patient user fixture for appointment references.
    """
    patient = User(
        email="patient@example.com",
        password_hash="patient_pass",
        role="patient",
        first_name="Patient",
        last_name="One",
        phone_number="1112223333",
        address="1 Patient Lane",
        emergency_contact=EmergencyContact(
            name="Mom", relationship="Parent", phone_number="9999999999"
        ),
    ).save()

    doctor = User(
        email="doctor@example.com",
        password_hash="doctor_pass",
        role="doctor",
        first_name="Doctor",
        last_name="Strange",
        phone_number="8887776666",
        address="1 Doctor Way",
        emergency_contact=EmergencyContact(
            name="Sister", relationship="Relative", phone_number="1231231234"
        ),
    ).save()

    return doctor, patient


def test_create_valid_appointment(db, doctor_and_patient):
    doctor, patient = doctor_and_patient
    appointment_time = datetime(2025, 1, 1, 10, 0, 0, tzinfo=UTC)

    appt = Appointment(patient_id=patient, doctor_id=doctor, appointment_time=appointment_time)
    appt.save()
    assert appt.id is not None
    assert appt.appointment_status == "scheduled"
    assert appt.created_at is not None
    assert appt.updated_at is not None


def test_appointment_invalid_status(db, doctor_and_patient):
    doctor, patient = doctor_and_patient
    appointment_time = datetime(2025, 1, 1, 10, 0, 0, tzinfo=UTC)

    appt = Appointment(
        patient_id=patient,
        doctor_id=doctor,
        appointment_time=appointment_time,
        appointment_status="invalid_status",
    )
    with pytest.raises(ValidationError):
        appt.save()


def test_appointment_save_updates_timestamp(db, doctor_and_patient):
    doctor, patient = doctor_and_patient
    appointment_time = datetime(2025, 1, 2, 14, 30, 0, tzinfo=UTC)

    appt = Appointment(patient_id=patient, doctor_id=doctor, appointment_time=appointment_time)
    appt.save()

    original_updated_at = appt.updated_at
    appt.reason = "Patient Follow-up"
    appt.save()

    assert appt.updated_at != original_updated_at


def test_appointment_missing_required_field(db):
    """
    Attempting to create an appointment without patient_id should fail.
    """
    appt = Appointment(doctor_id=None, appointment_time=datetime.now(UTC))  # Invalid
    with pytest.raises(ValidationError):
        appt.save()
