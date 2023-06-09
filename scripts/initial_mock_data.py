"""Scrpit to create base mock data"""
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from apps.authenticate.models import Clinic, User, License, Module
from utils.generators import generate_clinic_code, generate_license_code
from utils.constants import (
    USER,
    BILLING,
    CLINICAL,
    EXTRA,
    FINANCY,
    MARKETING,
    SCHEDULER,
)


def run():
    """Exceute create base mock data"""
    user, _ = User.objects.get_or_create(
        username="admin_test",
        email="admin@exemple.com",
        taxpayer_identification="1111111111111",
        defaults={
            "full_name": "Admin Teste",
            "is_staff": True,
        },
    )
    user.password = make_password("Test@123")
    user.save()

    user_clinic, _ = User.objects.get_or_create(
        username="clinic_manager_test",
        email="manager@example.com",
        taxpayer_identification="2222222222222",
        defaults={"full_name": "Clinic manager Teste", "is_clinic": True},
    )
    user_clinic.password = make_password("Test@123")
    user_clinic.save()

    license_obj, _ = License.objects.get_or_create(
        code=generate_license_code(), defaults={"name": "Licença teste"}
    )

    for module in [USER, BILLING, CLINICAL, EXTRA, FINANCY, MARKETING, SCHEDULER]:
        Module.objects.get_or_create(module=module, defaults={"license": license_obj})

    clinic, _ = Clinic.objects.get_or_create(
        taxpayer_identification="11111111111111111111",
        defaults={
            "code": generate_clinic_code(),
            "company_name": "Clínica teste",
            "license": license_obj,
            "domain_url": "apiteste",
            "schema_name": "test",
        },
    )

    clinic.account.add(user_clinic)
