"""Authenticate app config file"""
from django.apps import AppConfig


class AuthenticateConfig(AppConfig):
    """Authenticate config"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.authenticate"
    label = "authenticate"
