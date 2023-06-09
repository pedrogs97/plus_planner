"""Class of authenticate module view"""
from knox.auth import TokenAuthentication
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from apps.authenticate.serializers.auth import UserSerializer, ClinicSerialzier
from apps.authenticate.models import User, Clinic
from utils.custom_permissions import CustomDjangoModelPermissions


class UsersAdminViewset(ModelViewSet):
    """All users views for admins."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = IsAdminUser
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserViewset(ModelViewSet):
    """All users views for clinics."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ClinicAdminViewset(ModelViewSet):
    """All clinics views for admins."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = IsAdminUser
    serializer_class = ClinicSerialzier
    queryset = Clinic.objects.all()


class ClinicViewset(ModelViewSet):
    """All clinic views for clinics."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = ClinicSerialzier
    queryset = Clinic.objects.all()
