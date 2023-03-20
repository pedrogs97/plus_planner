"""Scheduler app config file"""
from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    """Scheduler app config file"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.scheduler"
    label = "scheduler"
