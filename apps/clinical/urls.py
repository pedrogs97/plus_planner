"""Clinical module URLs"""
from django.urls import include, path

from rest_framework import routers
from apps.clinical.views import (
    DeskViewSet,
    PacientViewSet,
    PlanAdminViewSet,
    PlanViewSet,
)

app_name = "clinical"

router = routers.DefaultRouter()
router.register(r"desks", DeskViewSet)
router.register(r"pacients", PacientViewSet)
router.register(r"plans-admin", PlanAdminViewSet)
router.register(r"plans", PlanViewSet)

urlpatterns = [path("clinical/", include(router.urls))]
