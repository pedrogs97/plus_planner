"""Authenticate serializers"""
from rest_framework import serializers

from apps.authenticate.models import Clinic, License, Module
from utils.generators import generate_clinic_code, generate_license_code


class ClinicSerialzier(serializers.ModelSerializer):
    """
    Clinic Serializer.

    Serialize all fields
    """

    is_branch = serializers.SerializerMethodField()

    class Meta:
        """Meta class"""

        model = Clinic
        field = [
            "company_name",
            "code",
            "taxpayer_identification",
            "natural_person",
            "account",
            "headquarters",
            "license",
            "is_branch",
        ]

    def validate_code(self, _):
        """
        Code field validator.

        Just return a new code.
        """
        return generate_clinic_code()

    def get_is_branch(self, obj: Clinic):
        """Serialize is_branch property"""
        return str(obj.is_branch)


class ModuleSerializer(serializers.ModelSerializer):
    """
    Module Serializer.

    Serialize all fields
    """

    class Meta:
        """Meta class"""

        model = Module
        fields = "__all__"


class LicenseSerialzier(serializers.ModelSerializer):
    """
    License Serializer.

    Serialize all fields
    """

    modules = serializers.SerializerMethodField()

    class Meta:
        """Meta class"""

        model = License
        field = [
            "code",
            "validity",
            "trail",
            "payment_date",
            "modules",
        ]

    def validate_code(self, _):
        """
        Code field validtor.

        Just return a new code.
        """
        return generate_license_code()

    def get_modules(self, obj: License):
        return obj.modules
