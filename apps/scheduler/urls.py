from django.urls import include
from rest_framework import routers

from apps.scheduler.views import ScheduleEventViewset

router = routers.DefaultRouter()
router.register(r"schedule-event", ScheduleEventViewset)
urlpatterns = ["", include(router.urls)]
