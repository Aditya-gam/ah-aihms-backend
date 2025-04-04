# app/models/__init__.py
# fmt: off
# NOTE: This file is excluded from auto-formatting tools (black, isort, ruff)
# The import order here is deliberate and should not be changed
from .analytics_data import AnalyticsData
from .appointment import Appointment
from .medical_record import MedicalRecord
from .user import User

__all__ = ["User", "Appointment", "MedicalRecord", "AnalyticsData"]
# fmt: on
