"""Class of Clinical module views"""
from knox.auth import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from apps.clinical.serializers import DeskSerializer, PlanSerializer, PacientSerializer
from apps.clinical.models import Desk, Plan, Pacient
from utils.custom_permissions import CustomDjangoModelPermissions


class PlanAdminViewSet(ModelViewSet):
    """All plans views for admins."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = IsAdminUser
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()


class PlanViewSet(ModelViewSet):
    """All plans views for clinics."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()


class DeskViewSet(ModelViewSet):
    """All desks views for clinics."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = DeskSerializer
    queryset = Desk.objects.all()


class PacientViewSet(ModelViewSet):
    """All pacients views for clinics."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = PacientSerializer
    queryset = Pacient.objects.all()
