from rest_framework.serializers import ModelSerializer

from apps.scheduler.models import ScheduleEvent


class ScheduleEventSerializer(ModelSerializer):
    """
    Schedule event serializer.

    Create, update and get.
    """

    class Meta:
        """
        Class Meta
        """

        model = ScheduleEvent
        field = "__all__"
