"""Authenticate URLs"""
from django.urls import include, path

from apps.authenticate.views.auth import LoginView
from apps.authenticate.views.user import UsersView, UserView

app_name = "authenticate"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("users/", UsersView.as_view(), name="users_view"),
    path("user/<str:pk>/", UserView.as_view(), name="user_view"),
]

urlpatterns = [path("authenticate/", include(urlpatterns))]
