"""Clinical app config file"""
from django.apps import AppConfig


class ClinicalConfig(AppConfig):
    """Clinical config"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.clinical"
    label = "clinical"
