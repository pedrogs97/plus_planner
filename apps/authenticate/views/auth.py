"""Auth views of Authenticate module"""
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


class LoginView(KnoxLoginView):
    """Login view"""

    authentication_classes = None
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """Override login with clinic"""
        # TODO validate clinic for login
        token_limit_per_user = self.get_token_limit_per_user()
        if token_limit_per_user is not None:
            now = timezone.now()
            token = request.user.auth_token_set.filter(expiry__gt=now)
            if token.count() >= token_limit_per_user:
                return Response(
                    {"error": "Maximum amount of tokens allowed per user exceeded."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(request.user, token_ttl)
        user_logged_in.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        data = self.get_post_response_data(request, token, instance)
        return Response(data)
