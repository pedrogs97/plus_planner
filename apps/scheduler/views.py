"""Schedule event views of Scheduler module"""
from rest_framework.viewsets import ModelViewSet
from knox.auth import TokenAuthentication
from apps.scheduler.serializers import ScheduleEventSerializer
from utils.custom_permissions import (
    CustomDjangoModelPermissions,
    IsOwner,
)


class ScheduleEventViewset(ModelViewSet):
    """
    Schedule event views

    POST, GET, UPDATE and DELETE
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomDjangoModelPermissions, IsOwner)
    serializer_class = ScheduleEventSerializer
