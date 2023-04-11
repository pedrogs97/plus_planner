"""Authenticate serializers for auth"""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.hashers import make_password

# from django.contrib import auth
# from django.contrib.auth.models import Group, Permission
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.encoding import force_str
# from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers

from apps.authenticate.models import User
from apps.authenticate.serializers.credentials import ClinicSerialzier
from utils.base.serializers import DynamicFieldsModelSerializer
from utils.email_sender import SendinblueEmailSender

# from rest_framework.exceptions import AuthenticationFailed


class UserSerializer(DynamicFieldsModelSerializer):
    """
    Serializer for create and update User
    """

    clinics = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

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
            if (isinstance(settings.SPECIAL_CHAR, list))
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
                    f"This password is too short. It must contain at least \
                    {self.min_length} character."
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
                    "This password has no special characters. It must contain at least \
                    special character. "
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

    def get_clinics(self, obj: User):
        """List of user clinic serialized"""
        return ClinicSerialzier(obj.get_clinics(), many=True).data

    def get_permissions(self, obj: User):
        """List of user permissions serialized"""
        return obj.get_user_permissions()


class LoginSerializer(serializers.Serializer):
    """
    Login serializer

    Validate email and password
    """

    email = serializers.EmailField(required=True, allow_blank=False)
    clinic_code = serializers.IntegerField(required=True)
    password = serializers.CharField(
        required=True, style={"input_type": "password"}, allow_blank=False
    )

    def validate(self, attrs):
        email = attrs.pop("email", "")
        clinic_code = attrs.pop("clinc_id", "")
        password = attrs.pop("password", "")
        if email == "" or clinic_code == "" or password == "":
            msg = _("No credentials provided.")
            raise ValidationError(msg)
        try:
            user = User.objects.get(email=email, clinic__code=clinic_code)
        except User.DoesNotExist as user_does_not_exist:
            msg = _("Unable to log in with provided credentials.")
            raise ValidationError(msg) from user_does_not_exist

        if not user:
            msg = _("Unable to log in with provided credentials.")
            raise ValidationError(msg)
        return {"user": user}

    def create(self, validated_data):
        """Not implmented"""
        return None

    def update(self, instance, validated_data):
        """Not implmented"""
        return None


class ChangePasswordSerializer(serializers.Serializer):
    """Change password Serializer"""

    user_id = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        """Meta Class"""

        fields = ["current_password", "new_password"]

    def validate(self, attrs):
        user = User.objects.get(id=attrs["user_id"])
        if user.check_password(attrs["current_password"]):
            return attrs

        msg = _("Unable to change password.")
        raise ValidationError(msg)

    def create(self, validated_data):
        """Applies new password"""
        user = User.objects.get(id=validated_data["user_id"])
        user.password = make_password(validated_data["new_password"])
        return {}

    def update(self, instance, validated_data):
        """Not implmented"""
        return {}


# class EmailVerificationSerializer(serializers.Serializer):
#     token = serializers.CharField(max_length=555)

#     class Meta:
#         fields = ["token"]


class ForgotPasswordSerializer(serializers.Serializer):
    """Forgot password Serializer"""

    email = serializers.EmailField(min_length=2, required=True)
    clinic_code = serializers.IntegerField(required=True)

    class Meta:
        """Meta Class"""

        fields = ["email", "clinic_code"]

    def create(self, validated_data):
        """Applies new password"""
        try:
            user = User.objects.get(
                email=validated_data["email"],
                clinic__code=validated_data["clinic_code"],
            )
            email_sender = SendinblueEmailSender()
            email_sender.build_email(
                {
                    "html_content": "<html><body><h1>Teste pela classe</h1></body></html>",
                    "subject": "Testando",
                },
                {"name": "Sendinblue", "email": "contact@sendinblue.com"},
                {"name": "Sendinblue", "email": "contact@sendinblue.com"},
                [{"name": user.full_name, "email": user.email}],
            )
            email_sender.send_email()
        except User.DoesNotExist:
            return {}
        return {}

    def update(self, instance, validated_data):
        """Not implmented"""
        return {}


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
