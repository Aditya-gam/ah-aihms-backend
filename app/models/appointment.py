"""
Appointment Schema

This schema represents an appointment between a patient and a doctor.
Includes references to users, appointment scheduling details, and status management.

Indexes:
- Compound index on (doctor_id, appointment_time)
    for fast retrieval of doctor's appointments.
- Compound index on (patient_id, appointment_time)
    for efficient retrieval of patient's appointments.
"""

from datetime import UTC, datetime

from app import db


class Appointment(db.Document):
    """
    MongoEngine document schema for Appointments.
    """

    # Possible statuses of an appointment
    STATUS_CHOICES = ("scheduled", "completed", "cancelled", "rescheduled")

    # Reference to the patient (User schema)
    patient_id = db.ReferenceField(
        "User",
        required=True,
        reverse_delete_rule=db.CASCADE,
        help_text="The patient attending the appointment.",
    )

    # Reference to the doctor (User schema)
    doctor_id = db.ReferenceField(
        "User",
        required=True,
        reverse_delete_rule=db.CASCADE,
        help_text="The doctor who will conduct the appointment.",
    )

    # Date and time of the appointment
    appointment_time = db.DateTimeField(
        required=True, help_text="Scheduled date and time of the appointment."
    )

    # Current status of the appointment
    appointment_status = db.StringField(
        required=True,
        choices=STATUS_CHOICES,
        default="scheduled",
        help_text="The current status of the appointment.",
    )

    # Reason or description for the appointment
    reason = db.StringField(
        required=False,
        help_text="Optional reason provided by the patient for the appointment.",
    )

    # Timestamp when the appointment record was created
    created_at = db.DateTimeField(
        default=lambda: datetime.now(UTC),
        help_text="The creation timestamp of the appointment record.",
    )

    # Timestamp when the appointment was last updated
    updated_at = db.DateTimeField(
        default=lambda: datetime.now(UTC),
        help_text="The timestamp of the most recent update.",
    )

    # Metadata including indexes for optimized queries
    meta = {
        "indexes": [
            {
                "fields": ["doctor_id", "appointment_time"],
                "name": "doctor_appointment_idx",
            },
            {
                "fields": ["patient_id", "appointment_time"],
                "name": "patient_appointment_idx",
            },
        ],
        "ordering": ["-appointment_time"],
        "collection": "appointments",
    }

    def save(self, *args, **kwargs):
        """
        Overrides default save method to update the 'updated_at' timestamp automatically.
        """
        self.updated_at = datetime.now(UTC)
        return super(Appointment, self).save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the Appointment.
        """
        appointment_time = self.appointment_time.strftime("%Y-%m-%d %H:%M:%S")
        appointment_status = self.appointment_status.capitalize()
        appointment_id = self.id
        appointment_patient = self.patient_id
        appointment_doctor = self.doctor_id

        return (
            f"Appointment({appointment_id}): {appointment_patient} with "
            f"{appointment_doctor} at {appointment_time}[{appointment_status}]"
        )
