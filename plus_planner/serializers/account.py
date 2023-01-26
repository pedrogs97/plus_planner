"""
Account serializers
"""
# from django.contrib import auth
# from django.contrib.auth.models import Group, Permission
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.encoding import force_str
# from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.conf import settings
from rest_framework import serializers

# from rest_framework.exceptions import AuthenticationFailed

from plus_planner.models.account import User, Role
from plus_planner.serializers.dynamic import DynamicFieldsModelSerializer


class UserSerializer(DynamicFieldsModelSerializer):
    """
    Serializer for create and update User
    """

    class Meta:
        """
        Class Meta
        """

        model = User
        extra_kwargs = {"password": {"write_only": True}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_length = (
            8
            if (settings.MIN_LENGTH_PASSWORD is None)
            else settings.MIN_LENGTH_PASSWORD
        )
        self.special_chars = (
            ["!", "@", "#", "_", ".", "+", "-", "*"]
            if (type(settings.SPECIAL_CHAR) is not list)
            or (settings.SPECIAL_CHAR is None)
            else settings.SPECIAL_CHAR
        )

    def validate_password(self, new_pass):
        """
        Validate password field before save
        """
        if new_pass.isdigit():
            raise ValidationError(
                _("This password is entirely numeric."),
                code="password_entirely_numeric",
            )
        if len(new_pass) < self.min_length:
            raise ValidationError(
                _(
                    f"This password is too short. It must contain at least {self.min_length} character."
                ),
                code="password_too_short",
            )
        valid = False
        for special_char in self.special_chars:
            if special_char in new_pass:
                valid = True
                break
        if not valid:
            raise ValidationError(
                _(
                    "This password has no special characters. It must contain at least special character. "
                    + ",".join(self.special_chars)
                ),
                code="password_without_special_char",
            )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password and instance.check_password(password):
            instance.set_password(validated_data["password"])
        instance = super().update(instance, validated_data)
        return instance


class RolesSerialzier(serializers.Serializer):
    """
    Serializer for return one or all roles
    """

    id = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=20)

    class Meta:
        """
        Class Meta
        """

        model = Role

    def create(self, validated_data):
        """
        Not implemented
        """
        return None

    def update(self, instance, validated_data):
        """
        Not implemented
        """
        return None


# class EmailVerificationSerializer(serializers.Serializer):
#     token = serializers.CharField(max_length=555)

#     class Meta:
#         fields = ["token"]


# class PasswordResetLinkSerializer(serializers.Serializer):
#     email = serializers.EmailField(min_length=2)
#     username = serializers.CharField(min_length=3, max_length=255)

#     class Meta:
#         fields = ["email", "username"]


# class NewPasswordSerializer(serializers.Serializer):
#     password = serializers.CharField(min_length=6, max_length=68, write_only=True)
#     token = serializers.CharField(min_length=1, write_only=True)
#     uidb64 = serializers.CharField(min_length=1, write_only=True)

#     class Meta:
#         fields = ["password", "token", "id"]

#     def create(self, validated_data):
#         try:
#             password = validated_data.get("password")
#             token = validated_data.get("token")
#             uidb64 = validated_data.get("uidb64")
#             id = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=id)
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 raise AuthenticationFailed("The reset link is invalid", 401)
#             user.set_password(password)
#             user.save()

#             return {"message": "Password changed successfully"}
#         except User.DoesNotExist:
#             raise AuthenticationFailed("The reset link is invalid", 401)
