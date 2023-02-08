"""
Class of account module view
"""
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import authentication
from rest_framework import status
from rest_framework_roles.granting import is_self
from plus_planner.models.account import User


class UsersView(GenericAPIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only manager users are able to access this view.
    """

    authentication_classes = [authentication.TokenAuthentication]
    view_permissions = {
        # "post": {"manager": True},
        "get": {"manager": True, "assistant": True},
        # "get,update,update_partial": {"manager": True, "assistant": True},
    }

    def get(self, request: Request, format=None):
        """
        Return a list of all users.
        """
        return Response(status=status.HTTP_200_OK)
