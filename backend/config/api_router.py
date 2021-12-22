from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from config.settings import DEBUG
from cubes.api.views import TestViewSet, RoomAPIViewSet

if DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register('tests', TestViewSet, basename="tests")
router.register('rooms', RoomAPIViewSet, basename="rooms")

urlpatterns = router.urls
