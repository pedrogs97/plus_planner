from django.contrib import auth
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from plus_planner.models.account import User
from plus_planner.serializers.dynamic import DynamicFieldsModelSerializer
from django.conf import settings


class LoginSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        fields = [
            "id",
            "username",
            "email",
            "password",
            "access_token",
            "refresh_token",
        ]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        try:
            user = auth.authenticate(
                username=User.objects.get(email=str(email)).username, password=password
            )
        except Exception:
            try:
                user = auth.authenticate(username=str(email), password=password)
            except Exception:
                try:
                    user = auth.authenticate(username=email, password=password)
                except Exception:
                    user = auth.authenticate(
                        username=User.objects.get(username=str(email)).email,
                        password=password,
                    )

        if not user:
            raise AuthenticationFailed(
                "Credenciais inválidas. Usuário ou senha incorretos."
            )

        if not user.is_active:
            raise AuthenticationFailed(
                "Credenciais inválidas. Usuário ou senha incorretos."
            )

        if not user.is_superuser:
            raise AuthenticationFailed(
                "Credenciais inválidas. Usuário ou senha incorretos."
            )

        token = user.get_tokens_for_user()
        return {
            "id": user.id,
            "username": user.username,
            "access_token": token.get("access"),
            "refresh_token": token.get("refresh"),
        }


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        exclude = ["created_at", "updated_at"]
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
                    + ",".join(self.special_chars, ",")
                ),
                code="password_without_special_char",
            )

    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.
        :param validated_data:
        """
        if validated_data["is_staff"]:
            validated_data.pop("is_staff")
            user = User.objects.create_superuser(**validated_data)
        else:
            validated_data.pop("is_staff")
            user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
            instance.save()
        return instance


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        fields = ["token"]


class PasswordResetLinkSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    username = serializers.CharField(min_length=3, max_length=255)

    class Meta:
        fields = ["email", "username"]


class NewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "id"]

    def create(self, validated_data):
        try:
            password = validated_data.get("password")
            token = validated_data.get("token")
            uidb64 = validated_data.get("uidb64")
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)
            user.set_password(password)
            user.save()

            return {"message": "Password changed successfully"}
        except User.DoesNotExist:
            raise AuthenticationFailed("The reset link is invalid", 401)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class PermissionSerializer(serializers.Serializer):
    class Meta:
        model = Permission
        fields = "__all__"
