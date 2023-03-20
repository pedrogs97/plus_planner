"""Extra app config file"""
from django.apps import AppConfig


class ExtraConfig(AppConfig):
    """Extra config"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.extra"
    label = "extra"
