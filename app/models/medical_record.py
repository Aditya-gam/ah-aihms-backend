"""
MedicalRecord Schema

This schema represents medical records uploaded to the system,
linking patient information with secure document storage, blockchain verification, and metadata.

Indexes:
- Index on patient_id for quick retrieval of patient-specific medical records.
"""

from datetime import datetime

from app import db


class MedicalRecord(db.Document):
    """
    MongoEngine document schema for Medical Records.
    """

    # Predefined record types to ensure consistency across records
    RECORD_TYPES = ("report", "prescription", "imaging")

    # Patient associated with this medical record
    patient_id = db.ReferenceField(
        "User",
        required=True,
        reverse_delete_rule=db.CASCADE,
        help_text="Reference to the patient this medical record belongs to.",
    )

    # Doctor or authorized medical personnel who uploaded this record
    uploaded_by = db.ReferenceField(
        "User",
        required=True,
        reverse_delete_rule=db.SET_NULL,
        help_text="Reference to the doctor or medical personnel who uploaded the record.",
    )

    # Immutable blockchain hash/reference verifying the integrity of this medical record
    document_hash = db.StringField(
        required=True,
        unique=True,
        help_text="Blockchain-generated hash verifying the document's authenticity and integrity.",
    )

    # Type of medical record being stored
    record_type = db.StringField(
        required=True,
        choices=RECORD_TYPES,
        help_text="Type of the medical record (e.g., report, prescription, imaging).",
    )

    # Optional textual description of the medical record
    description = db.StringField(
        required=False, help_text="Brief description or notes about the medical record."
    )

    # Timestamp when the record was uploaded
    upload_date = db.DateTimeField(
        default=datetime.utcnow,
        help_text="Timestamp indicating when this medical record was uploaded.",
    )

    # Encrypted URL or reference pointing to the stored medical file
    file_url = db.StringField(
        required=True,
        help_text="Encrypted URL or storage reference to the actual medical record file.",
    )

    # Metadata and indexing configuration
    meta = {
        "indexes": [
            {"fields": ["patient_id"], "name": "patient_medical_records_idx"},
            {
                "fields": ["document_hash"],
                "unique": True,
                "name": "unique_document_hash_idx",
            },
        ],
        "ordering": ["-upload_date"],
        "collection": "medical_records",
    }

    def __str__(self):
        """
        Human-readable representation of the MedicalRecord instance.
        """
        return (
            f"MedicalRecord({self.id}): {self.record_type.capitalize()} "
            f"for Patient({self.patient_id.id}) uploaded by Doctor({self.uploaded_by.id}) "
            f"on {self.upload_date.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    def clean(self):
        """
        Additional validation or cleaning before saving the document.
        Ensures the file_url field follows
        encryption guidelines (placeholder for actual encryption checks).
        """
        # Example placeholder validation logic for encrypted URL
        if not self.file_url.startswith("https://"):
            raise db.ValidationError("The 'file_url' must be an encrypted HTTPS URL.")
