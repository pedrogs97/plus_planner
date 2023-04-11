"""Class of authenticate module view"""
from apps.authenticate.serializers.auth import UserSerializer
from utils.base.views import BaseListCreateView, BaseRetrieveUpdateDestroyView


class UsersView(BaseListCreateView):
    """View to list all users and create a new user of clinic."""

    serializer_class = UserSerializer


class UserView(BaseRetrieveUpdateDestroyView):
    """View to get, update and destroy a user of clinic."""

    serializer_class = UserSerializer
