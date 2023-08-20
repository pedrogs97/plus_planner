"""Authenticate URLs"""
from django.urls import include, path

from knox import views as knox_views
from rest_framework import routers
from apps.authenticate.views.auth import LoginView
from apps.authenticate.views.credentials import (
    UsersAdminViewset,
    UserViewset,
    ClinicViewset,
    ClinicAdminViewset,
)

app_name = "authenticate"

router = routers.DefaultRouter()
router.register(r"users-admin/", UsersAdminViewset)
router.register(r"users/", UserViewset)
router.register(r"clinics-admin/", ClinicAdminViewset)
router.register(r"clinics/", ClinicViewset)


urlpatterns = [
    path(r"login/", LoginView.as_view(), name="login"),
    path(r"logout/", knox_views.LogoutView.as_view(), name="logout"),
    path(r"logoutall/", knox_views.LogoutAllView.as_view(), name="logout_all"),
    path(r"", include(router.urls)),
]


urlpatterns = [path("authenticate/", include(urlpatterns))]
