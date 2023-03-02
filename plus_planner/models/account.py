"""
Account models
"""
import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

from plus_planner.utils.overwrite_image import OverwriteImage, upload_to
from plus_planner.utils.constants import (
    MANAGER,
    DOCTOR,
    ASSISTANT,
    NURSE,
    STR_ASSISTANT,
    STR_DOCTOR,
    STR_MANAGER,
    STR_NURSE,
)


class User(AbstractBaseUser):
    """
    User model
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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

    def __str__(self) -> str:
        return f"{self.username}"

    def get_tokens_for_user(self):
        """
        Get user tokens. Refresh token and access token.
        """
        refresh = RefreshToken.for_user(self)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes. Update password
        """
        return check_password(raw_password, self.password)

    def get_roles_by_clinic(self, clinic_id: str) -> list:
        """
        Returns user role given specific clinic
        """
        user_roles = ClinicUserRole.objects.only("role_type").filter(
            user_id=self.id, clinic_id=clinic_id
        )
        if not user_roles.exists():
            return []
        return [user_role.role_type for user_role in user_roles]

    def get_all_roles(self) -> list:
        """
        Returns user role from all linked clinics
        """
        user_roles = ClinicUserRole.objects.only("clinic", "role_type").filter(
            user_id=self.id
        )
        if not user_roles.exists():
            return []
        return [
            {
                "clinic": user_role.clinic.company_name,
                "role_type": user_role.role_type,
            }
            for user_role in user_roles
        ]

    def get_clinics(self) -> list:
        """
        Returns user clinic
        """
        user_roles = ClinicUserRole.objects.only("clinic").filter(user_id=self.id)
        if not user_roles.exists():
            return []
        return [user_role.clinic for user_role in user_roles]


class Clinic(models.Model):
    """
    Clinic model
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=255)
    taxpayer_identification = models.CharField(max_length=20, unique=True)
    subsidiary = models.BooleanField(default=False)
    natural_person = models.BooleanField(default=False)
    account = models.ManyToManyField(
        User,
        through="ClinicUserRole",
        through_fields=("clinic", "user"),
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
            f"{self.company_name} - filial"
            if self.subsidiary
            else f"{self.company_name} - matriz"
        )


class ClinicUserRole(models.Model):
    """
    Through model for Clinic and User many to many relationship
    """

    ROLES_CHOICES = [
        (MANAGER, STR_MANAGER),
        (DOCTOR, STR_DOCTOR),
        (ASSISTANT, STR_ASSISTANT),
        (NURSE, STR_NURSE),
    ]

    PAIR_ROLE_KEY_VALUE = {
        MANAGER: STR_MANAGER,
        DOCTOR: STR_DOCTOR,
        ASSISTANT: STR_ASSISTANT,
        NURSE: STR_NURSE,
    }

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role_type = models.PositiveSmallIntegerField(choices=ROLES_CHOICES)

    class Meta:
        """
        Through Class Meta
        """

        db_table = "clinic_role"
        verbose_name = "clinic_role"
        verbose_name_plural = "clinic_roles"

    def __str__(self) -> str:
        return f"{self.user.__str__()} : {self.clinic.__str__()}\
                 : {self.PAIR_ROLE_KEY_VALUE[self.role_type]}"
