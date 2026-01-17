from django.urls import include, path
from rest_framework.routers import DefaultRouter

from habitica.views import HabitViewSet

app_name = "habitica"

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habits")

urlpatterns = [
    path("", include(router.urls)),
] + router.urls
