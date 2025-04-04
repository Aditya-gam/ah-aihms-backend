# app/models/__init__.py
# isort: skip_file
# fmt: off
# NOTE: This file is excluded from auto-formatting tools (black, isort, ruff)
# The import order here is deliberate and should not be changed
from .user import User
from .analytics_data import AnalyticsData
from .appointment import Appointment
from .medical_record import MedicalRecord

__all__ = ["User", "Appointment", "MedicalRecord", "AnalyticsData"]
# fmt: on
