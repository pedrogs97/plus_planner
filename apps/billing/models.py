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
