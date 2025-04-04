import pytest
from mongoengine import NotUniqueError, ValidationError

from app.models.medical_record import MedicalRecord
from app.models.user import EmergencyContact, User


@pytest.fixture
def doctor_and_patient(db):
    """
    Reuse fixture for creating a doctor and a patient user.
    """
    patient = User(
        email="medpatient@example.com",
        password_hash="patient_pass",
        role="patient",
        first_name="Med",
        last_name="Patient",
        phone_number="9992223333",
        address="1 Med Lane",
        emergency_contact=EmergencyContact(
            name="Guardian", relationship="Guardian", phone_number="0001112222"
        ),
    ).save()

    doctor = User(
        email="meddoctor@example.com",
        password_hash="doctor_pass",
        role="doctor",
        first_name="Med",
        last_name="Doctor",
        phone_number="8887776666",
        address="1 Doctor Blvd",
        emergency_contact=EmergencyContact(
            name="Sibling", relationship="Sibling", phone_number="1231231234"
        ),
    ).save()

    return doctor, patient


def test_create_valid_medical_record(db, doctor_and_patient):
    doctor, patient = doctor_and_patient
    record = MedicalRecord(
        patient_id=patient,
        uploaded_by=doctor,
        document_hash="unique_doc_hash_123",
        record_type="report",
        file_url="https://valid-secure-url.com/report.pdf",
    )
    record.save()
    assert record.id is not None
    assert record.record_type == "report"
    assert record.file_url.startswith("https://")


def test_duplicate_document_hash(db, doctor_and_patient):
    doctor, patient = doctor_and_patient
    MedicalRecord(
        patient_id=patient,
        uploaded_by=doctor,
        document_hash="unique_doc_hash_999",
        record_type="imaging",
        file_url="https://my-url.com/scan.jpg",
    ).save()

    # Attempt with duplicate hash
    with pytest.raises(NotUniqueError):
        MedicalRecord(
            patient_id=patient,
            uploaded_by=doctor,
            document_hash="unique_doc_hash_999",
            record_type="prescription",
            file_url="https://my-url.com/prescription.jpg",
        ).save()


def test_missing_https_url(db, doctor_and_patient):
    doctor, patient = doctor_and_patient
    record = MedicalRecord(
        patient_id=patient,
        uploaded_by=doctor,
        document_hash="some_hash_456",
        record_type="report",
        file_url="http://insecure.com/file.pdf",  # Insecure URL
    )
    with pytest.raises(ValidationError):
        record.save()


def test_invalid_record_type(db, doctor_and_patient):
    doctor, patient = doctor_and_patient
    record = MedicalRecord(
        patient_id=patient,
        uploaded_by=doctor,
        document_hash="valid_hash_789",
        # Not one of (report, prescription, imaging)
        record_type="invalid_type",
        file_url="https://secure.com/data.pdf",
    )
    with pytest.raises(ValidationError):
        record.save()
