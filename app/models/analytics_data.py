"""
AnalyticsData Schema

Stores predictive health analytics data and patient metrics generated by AI models,
providing structured insights into patient health status over time.

Indexes:
- Index on patient_id for efficient retrieval of patient-specific analytics data.
"""

from datetime import UTC, datetime

from app import db


class AnalyticsData(db.Document):
    """
    MongoEngine document schema for storing analytics and predictive health data.
    """

    # Reference to the patient associated with this analytics data
    patient_id = db.ReferenceField(
        "User",
        required=True,
        reverse_delete_rule=db.CASCADE,
        help_text="Reference to the patient for whom analytics data was generated.",
    )

    # Detailed nested metrics capturing patient health data (e.g., vital signs)
    # We keep required=True here so empty dict triggers "The 'metrics' field cannot be empty."
    metrics = db.DictField(
        required=True,
        help_text="Nested dictionary containing health metrics",
    )

    # Results from AI predictive models assessing risk factors or health conditions
    # CHANGED: removed required=True to let custom logic handle empty dict
    prediction_results = db.DictField(
        help_text="Nested dictionary with predictive analytics results",
    )

    # Identifier or name of the AI model that generated the predictions
    generated_by_model = db.StringField(
        required=True,
        help_text="Reference to the AI model used to generate these analytics and predictions.",
    )

    # Timestamp marking when this analytics data was generated
    generated_at = db.DateTimeField(
        default=lambda: datetime.now(UTC),
        help_text="Timestamp indicating when the analytics data was generated.",
    )

    # Metadata and indexing configuration
    meta = {
        "indexes": [
            {"fields": ["patient_id"], "name": "patient_analytics_data_idx"},
            {"fields": ["generated_at"], "name": "analytics_generated_at_idx"},
        ],
        "ordering": ["-generated_at"],
        "collection": "analytics_data",
    }

    def __str__(self):
        """
        Human-readable representation for logging, debugging, or administrative purposes.
        """
        generated_time = self.generated_at.strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"AnalyticsData({self.id}): Generated for Patient({self.patient_id.id}) "
            f"by Model '{self.generated_by_model}' at {generated_time}"
        )

    def clean(self):
        """
        Validates the integrity and structure of analytics data before saving.
        Ensures that required health metrics and predictions are properly structured.
        """
        # (1) Check that metrics is not empty (your existing domain logic).
        if not self.metrics:
            raise db.ValidationError("The 'metrics' field cannot be empty.")

        # (2) If no prediction_results field or it's empty, raise domain error
        # Instead of the default field-level message, we rely on custom logic:
        if not self.prediction_results:
            raise db.ValidationError("At least one predictive result must be provided.")

        # Example validation ensuring metrics include standard expected entries
        required_metric_keys = {"heart_rate", "blood_pressure", "glucose_level"}
        missing_metrics = required_metric_keys - self.metrics.keys()
        if missing_metrics:
            raise db.ValidationError(
                f"Missing essential health metrics: {', '.join(missing_metrics)}"
            )
