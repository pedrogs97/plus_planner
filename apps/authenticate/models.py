"""
Authenticate models
"""
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.db import models

from utils.base.mixins import BasePermissionsMixin
from utils.base.models import BaseModel
from utils.images import OverwriteImage, upload_to


class User(AbstractBaseUser, BaseModel, BasePermissionsMixin):
    """
    User model
    """

    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
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

    teams = models.ManyToManyField("Team")

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


class Clinic(BaseModel):
    """
    Clinic model
    """

    company_name = models.CharField(max_length=255)
    taxpayer_identification = models.CharField(max_length=20, unique=True)
    natural_person = models.BooleanField(default=False)
    account = models.ManyToManyField(User)
    headquarters = models.ForeignKey(
        "self", related_name="branch", null=True, on_delete=models.PROTECT
    )

    class Meta:
        """
        Clinic Class Meta
        """

        db_table = "clinic"
        verbose_name = "clinic"
        verbose_name_plural = "clinics"

    def __str__(self) -> str:
        return (
            f"{self.company_name} - filial de {self.headquarters}"
            if self.is_subsidiary
            else f"{self.company_name} - matriz"
        )

    @property
    def is_subsidiary(self) -> bool:
        """Returns if is subsidiary clinic"""
        return self.headquarters is not None


class Team(Group):
    """Custom group model"""

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=False)

    class Meta:
        """
        Team Class Meta
        """

        db_table = "team"
        verbose_name = "team"
        verbose_name_plural = "teams"
