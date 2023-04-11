"""Project code generators"""
import random

from apps.authenticate.models import Clinic, License
from utils.constants import (
    MAX_CLINIC_CODE,
    MAX_LICENSE_CODE,
    MIN_CLINIC_CODE,
    MIN_LICENSE_CODE,
)


def generate_license_code() -> int:
    """Generate unique code"""
    can_create = False

    while not can_create:
        try:
            code = random.randint(MIN_LICENSE_CODE, MAX_LICENSE_CODE)
            License.objects.get(code=code)
        except License.DoesNotExist:
            can_create = True

    return code


def generate_clinic_code() -> int:
    """Generate unique code"""
    can_create = False

    while not can_create:
        try:
            code = random.randint(MIN_CLINIC_CODE, MAX_CLINIC_CODE)
            Clinic.objects.get(code=code)
        except Clinic.DoesNotExist:
            can_create = True

    return code
