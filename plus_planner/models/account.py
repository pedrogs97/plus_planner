import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    Group,
    PermissionsMixin,
    UserManager,
)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from utils.overwrite_image import OverwriteImage, upload_to


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    taxpayer_identification = models.CharField(max_length=13, unique=True)
    image = models.ImageField(
        null=True, storage=OverwriteImage(), upload_to=upload_to, max_length=255
    )
    # permissions
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # revoke permissions
    groups = None
    user_permissions = None

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "full_name", "taxpayer_identification"]

    class Meta:
        db_table = "user"
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return f"{self.full_name} - {self.email}"

    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class Clinic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=255)
    taxpayer_identification = models.CharField(max_length=20, unique=True)
    subsidiary = models.BooleanField(default=False)
    natural_person = models.BooleanField(default=False)
    account = models.ManyToManyField(User)

    class Meta:
        db_table = "clinic"
        verbose_name = "clinic"
        verbose_name_plural = "clinics"

    def __str__(self):
        return self.company_name


class Group(Group):
    clinic = models.OneToOneField(
        Clinic, on_delete=models.PROTECT, related_name="group"
    )

    class Meta:
        db_table = "group"
        verbose_name = "group"
        verbose_name_plural = "groups"
