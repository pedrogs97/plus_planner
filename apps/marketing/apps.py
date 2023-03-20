"""Marketing app config file"""
from django.apps import AppConfig


class MarketingConfig(AppConfig):
    """Marketing app config file"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.marketing"
    label = "marketing"
