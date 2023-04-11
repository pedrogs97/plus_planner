"""
Clinical models
"""
from datetime import datetime

from django.db import models
from tenant_schemas.models import TenantMixin

from apps.authenticate.models import Clinic
from utils.base.models import BaseModel
from utils.constants import FAMALE, MALE, OTHER, STR_FAMALE, STR_MALE, STR_OTHER


class Pacient(BaseModel, TenantMixin):
    """
    Pacient model
    """

    GENRE_CHOICES = (
        (MALE, STR_MALE),
        (FAMALE, STR_FAMALE),
        (OTHER, STR_OTHER),
    )

    PAIR_GENRE_KEY_VALUE = {
        MALE: STR_MALE,
        FAMALE: STR_FAMALE,
        OTHER: STR_OTHER,
    }

    full_name = models.CharField(max_length=50)
    taxypayer_identification = models.CharField(max_length=13)
    birth_date = models.DateField()
    genre = models.PositiveSmallIntegerField(choices=GENRE_CHOICES)

    class Meta:
        """
        Pacient Class Meta
        """

        db_table = "pacient"
        verbose_name = "pacient"
        verbose_name_plural = "pacient"

    def __str__(self) -> str:
        return f"{self.full_name} - {self.age}/{self.PAIR_GENRE_KEY_VALUE[self.genre]}"

    @property
    def age(self):
        """
        Return pacient age
        """
        today = datetime.today()
        age = (
            today.year
            - self.birth_date.year
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )
        return age


class Desk(BaseModel, TenantMixin):
    """
    Desk model
    """

    number = models.PositiveSmallIntegerField()
    vacation = models.BooleanField(default=True)
    observation = models.CharField(max_length=150)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    class Meta:
        """
        Desk Class Meta
        """

        db_table = "desk"
        verbose_name = "desk"
        verbose_name_plural = "desks"

    def __str__(self) -> str:
        return f"{self.number} - {self.vacation.__str__()}"
