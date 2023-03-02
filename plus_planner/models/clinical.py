"""
Clinical models
"""
import uuid
from django.db import models

from plus_planner.models.account import Clinic
from utils.constants import MALE, FAMALE, OTHER, STR_MALE, STR_FAMALE, STR_OTHER


class Pacient(models.Model):
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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()
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


class Desk(models.Model):
    """
    Desk model
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
