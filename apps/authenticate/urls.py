"""Authenticate URLs"""
from django.urls import include, path

from knox import views as knox_views
from apps.authenticate.views.auth import LoginView
from apps.authenticate.views.credentials import UsersView, UserView

app_name = "authenticate"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("users/", UsersView.as_view(), name="users_view"),
    path("user/<str:pk>/", UserView.as_view(), name="user_view"),
    path("logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
]

urlpatterns = [path("authenticate/", include(urlpatterns))]
