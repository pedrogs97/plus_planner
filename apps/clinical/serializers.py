"""
Clinical serializers
"""
from rest_framework.serializers import ModelSerializer

from apps.clinical.models import Pacient, Desk, Plan


class PacientSerializer(ModelSerializer):
    """
    Pacient serializer.

    Create, update and get.
    """

    class Meta:
        """
        Class Meta
        """

        model = Pacient
        field = "__all__"


class DeskSerializer(ModelSerializer):
    """
    Desk serializer.

    Create, update and get.
    """

    class Meta:
        """
        Class Meta
        """

        model = Desk
        field = "__all__"


class PlanSerializer(ModelSerializer):
    """
    Plan serializer.

    Create, update and get.
    """

    class Meta:
        """
        Class Meta
        """

        model = Plan
        field = "__all__"
