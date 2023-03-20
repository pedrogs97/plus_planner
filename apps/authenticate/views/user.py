"""Class of authenticate module view"""
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class UsersView(ListCreateAPIView):
    """View to list all users and create a new user in the system."""


class UserView(RetrieveUpdateDestroyAPIView):
    """View to get, update and destroy a user in the system."""
