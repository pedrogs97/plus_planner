"""
Schedule models
"""
import uuid
from datetime import datetime

from django.db import models

from apps.authenticate.models import Clinic, User
from apps.clinical.models import Desk, Pacient
from utils.constants import (
    CANCELED,
    CONFIRMED,
    FINISHED,
    SCHEDULED,
    STR_CANCELED,
    STR_CONFIRMED,
    STR_FINISHED,
    STR_SCHEDULED,
)


class ScheduleEvent(models.Model):
    """
    ScheduleEvent model
    """

    STATUS_SCHEDULE_CHOICES = (
        (SCHEDULED, STR_SCHEDULED),
        (CONFIRMED, STR_CONFIRMED),
        (CANCELED, STR_CANCELED),
        (FINISHED, STR_FINISHED),
    )

    PAIR_STATUS_SCHEDULE_KEY_VALUE = {
        SCHEDULED: STR_SCHEDULED,
        CONFIRMED: STR_CONFIRMED,
        CANCELED: STR_CANCELED,
        FINISHED: STR_FINISHED,
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.PositiveSmallIntegerField(
        choices=STATUS_SCHEDULE_CHOICES, default=SCHEDULED
    )
    date = models.DateTimeField(default=datetime.now())
    description = models.CharField(max_length=150, blank=True, null=True)
    is_return = models.BooleanField(default=False)
    day_off = models.BooleanField(default=False)
    off_reason = models.CharField(max_length=150, blank=True, null=True)
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    pacient = models.ForeignKey(Pacient, on_delete=models.CASCADE)
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE)

    class Meta:
        """
        ScheduleEvent Class Meta
        """

        db_table = "schedule_event"
        verbose_name = "schedule_event"
        verbose_name_plural = "schedule_events"

    def __str__(self) -> str:
        str_date = datetime.strftime(self.date, "%d/%m/%Y - %H:%M:%S")
        return f"{str_date} - {self.PAIR_STATUS_SCHEDULE_KEY_VALUE[self.status]}"
