"""
Authenticate models
"""

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import check_password
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.http.request import split_domain_port
from django.core.exceptions import ObjectDoesNotExist

from utils.base.mixins import BasePermissionsMixin
from utils.base.models import BaseModel
from utils.constants import (
    BILLING,
    CLINICAL,
    DICT_MODULE_TO_STRING,
    EXTRA,
    FINANCY,
    MARKETING,
    MAX_CLINIC_CODE,
    MIN_CLINIC_CODE,
    SCHEDULER,
    STR_BILLING,
    STR_CLINICAL,
    STR_EXTRA,
    STR_FINANCY,
    STR_MARKETING,
    STR_SCHEDULER,
    STR_USER,
    USER,
)
from utils.images import OverwriteImage, upload_to
from apps.billing.models import License

CLINIC_DOMAINS_CACHE = {}


class DomainManager(models.Manager):
    """Manager to hadle with domain"""

    use_in_migrations = True

    def _get_domain_by_id(self, clinic_id):
        if clinic_id not in CLINIC_DOMAINS_CACHE:
            clinic = self.get(pk=clinic_id)
            CLINIC_DOMAINS_CACHE[clinic_id] = clinic
            return CLINIC_DOMAINS_CACHE[clinic_id]

    def _get_domain_by_request(self, request):
        host = request.get_host()
        try:
            if host not in CLINIC_DOMAINS_CACHE:
                CLINIC_DOMAINS_CACHE[host] = self.get(domain__iexact=host)
            return CLINIC_DOMAINS_CACHE[host]
        except ObjectDoesNotExist:
            try:
                domain, _ = split_domain_port(host)
                if domain not in CLINIC_DOMAINS_CACHE:
                    CLINIC_DOMAINS_CACHE[domain] = self.get(domain__iexact=domain)
                return CLINIC_DOMAINS_CACHE[domain]
            except ObjectDoesNotExist:
                return None

    def get_current(self, request=None, clinic_id=None):
        """Rerturn currente domain"""
        if clinic_id:
            return self._get_domain_by_id(clinic_id)
        if request:
            return self._get_domain_by_request(request)

        return None

    def clear_cache(self):
        """Clear domians in cache"""
        global CLINIC_DOMAINS_CACHE
        CLINIC_DOMAINS_CACHE = {}

    def get_by_natural_key(self, domain):
        """Return clinic by domain"""
        return self.get(domain=domain)


class User(AbstractBaseUser, BaseModel, BasePermissionsMixin):
    """
    User model
    """

    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    taxpayer_identification = models.CharField(max_length=13, unique=True)
    image = models.ImageField(
        blank=True,
        null=True,
        storage=OverwriteImage(),
        upload_to=upload_to,
        max_length=255,
    )
    is_clinic = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"

    objects = BaseUserManager()

    class Meta:
        """
        User Class Meta
        """

        db_table = "user"
        verbose_name = "user"
        verbose_name_plural = "users"

    def check_password(self, raw_password) -> bool:
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes. Update password
        """
        return check_password(raw_password, self.password)

    def get_clinics(self) -> list:
        """
        Returns user clinic
        """
        clinics = Clinic.objects.filter(account__id=self.id)
        if not clinics.exists():
            return []
        return clinics


class Module(BaseModel):
    """Modules model"""

    MODULE_CHOICES = (
        (USER, STR_USER),
        (BILLING, STR_BILLING),
        (CLINICAL, STR_CLINICAL),
        (EXTRA, STR_EXTRA),
        (FINANCY, STR_FINANCY),
        (MARKETING, STR_MARKETING),
        (SCHEDULER, STR_SCHEDULER),
    )

    module = models.PositiveSmallIntegerField(unique=True, choices=MODULE_CHOICES)
    license = models.ForeignKey(License, on_delete=models.CASCADE)

    class Meta:
        """
        Modules Class Meta
        """

        db_table = "module"
        verbose_name = "module"
        verbose_name_plural = "modules"

    def __str__(self) -> str:
        return f"{DICT_MODULE_TO_STRING[self.module]}"


class Clinic(BaseModel):
    """
    Clinic model
    """

    company_name = models.CharField(max_length=255)
    code = models.PositiveIntegerField(
        unique=True,
        validators=[
            MaxValueValidator(MAX_CLINIC_CODE),
            MinValueValidator(MIN_CLINIC_CODE),
        ],
    )
    taxpayer_identification = models.CharField(max_length=20, unique=True)
    natural_person = models.BooleanField(default=False)
    account = models.ManyToManyField(User)
    headquarters = models.ForeignKey(
        "self", related_name="branch", null=True, on_delete=models.PROTECT
    )
    license = models.OneToOneField(License, on_delete=models.CASCADE)
    domain = models.CharField(max_length=150, unique=True, default="admin")

    objects = DomainManager()

    class Meta:
        """
        Clinic Class Meta
        """

        db_table = "clinic"
        verbose_name = "clinic"
        verbose_name_plural = "clinics"

    def __str__(self) -> str:
        return (
            f"{self.company_name} - Head:{self.headquarters}"
            if self.is_branch
            else f"{self.company_name}"
        )

    @property
    def is_branch(self) -> bool:
        """Returns if is branch clinic"""
        return self.headquarters is not None
