"""Billing app config file"""
from django.apps import AppConfig


class BillingConfig(AppConfig):
    """Billing config"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.billing"
    label = "billing"
