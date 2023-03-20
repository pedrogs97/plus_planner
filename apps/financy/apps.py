"""Financy app config file"""
from django.apps import AppConfig


class FinancyConfig(AppConfig):
    """Financy config"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.financy"
    label = "financy"
