"""
Clinical models
"""
from datetime import datetime

from django.db import models

from apps.authenticate.models import Clinic
from utils.base.models import BaseModel
from utils.constants import FAMALE, MALE, OTHER, STR_FAMALE, STR_MALE, STR_OTHER


class Pacient(BaseModel):
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
    treatments = models.ManyToManyField("clinical.Treatment")

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
            - self.birth_date.yearp
            - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        )
        return age


class Desk(BaseModel):
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


class Plan(BaseModel):
    """
    Plan model
    """

    name = models.CharField(max_length=50)
    number = models.PositiveSmallIntegerField()

    class Meta:
        """
        Plan Class Meta
        """

        db_table = "plan"
        verbose_name = "plan"
        verbose_name_plural = "plans"

    def __str__(self) -> str:
        return f"{self.name} - {self.number}"


class Treatment(BaseModel):
    """
    Treatment model
    """

    name = models.CharField(max_length=50)
    number = models.PositiveSmallIntegerField()
    description = models.CharField(max_length=50, default="")
    cost = models.DecimalField(decimal_places=2, max_digits=6, default=0.0)

    class Meta:
        """
        Treatment Class Meta
        """

        db_table = "treatment"
        verbose_name = "treatment"
        verbose_name_plural = "treatments"

    def __str__(self) -> str:
        return f"{self.name}/{self.number} - {self.cost}"


class Urgency(BaseModel):
    """
    Urgency model
    """

    date = models.DateField()
    description = models.CharField(max_length=50, default="")
    pacient = models.ForeignKey(Pacient, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)

    class Meta:
        """
        Urgency Class Meta
        """

        db_table = "urgency"
        verbose_name = "urgency"
        verbose_name_plural = "urgences"

    def __str__(self) -> str:
        return f"{self.description} - {self.date.strftime('%d/%m/%Y')}"
