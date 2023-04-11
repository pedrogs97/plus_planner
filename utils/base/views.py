"""Project base views"""
from knox.auth import TokenAuthentication
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    UpdateAPIView,
)

from utils.custom_permissions import (
    CustomDjangoModelPermissions,
    IsAdministrative,
    IsOwner,
)


class BaseListCreateView(ListCreateAPIView):
    """BaseView to list and create."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomDjangoModelPermissions,)


class BaseListCreateAdministrativeView(ListCreateAPIView):
    """BaseView to list and create by staff."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomDjangoModelPermissions, IsAdministrative)


class BaseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """BaseView to get, update and destroy."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomDjangoModelPermissions,)


class BaseRetrieveUpdateDestroyAdministrativeView(RetrieveUpdateDestroyAPIView):
    """BaseView to get, update and destroy by staff."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomDjangoModelPermissions, IsAdministrative)


class BaseRetrieveUpdateSelfView(RetrieveUpdateAPIView):
    """BaseView to get and update by self."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (CustomDjangoModelPermissions, IsOwner)


class BaseUpdateSelfView(UpdateAPIView):
    """BaseView to update by self."""

    authentication_classes = (TokenAuthentication,)
    permission_classes = IsOwner
