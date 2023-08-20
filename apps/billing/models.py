"""
Billing models
"""
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from utils.base.models import BaseModel
from utils.constants import (
    MAX_LICENSE_CODE,
    MIN_LICENSE_CODE,
)


class License(BaseModel):
    """License model"""

    code = models.PositiveIntegerField(
        unique=True,
        validators=[
            MaxValueValidator(MIN_LICENSE_CODE),
            MinValueValidator(MAX_LICENSE_CODE),
        ],
    )
    name = models.CharField(max_length=50)
    validity = models.DateField(null=True)
    trail = models.BooleanField(default=False)
    payment_date = models.DateField(null=True)
    value = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        """
        License Class Meta
        """

        db_table = "license"
        verbose_name = "license"
        verbose_name_plural = "licenses"

    @property
    def modules(self) -> list[str]:
        """Returns all modules(str) in license"""
        from apps.authenticate.models import Module

        return [str(module) for module in Module.objects.filter(license__id=self.id)]


class LicenseUser(BaseModel):
    """License user model"""

    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True)
    off_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    credit = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    user = models.ForeignKey(
        "authenticate.User",
        on_delete=models.DO_NOTHING,
        related_name="license",
    )
    license = models.ForeignKey(
        License, on_delete=models.DO_NOTHING, related_name="user_license"
    )


class History(BaseModel):
    """History model"""

    payment_date = models.DateField(null=True)
    user_license = models.ForeignKey(
        LicenseUser, on_delete=models.DO_NOTHING, related_name="history"
    )
