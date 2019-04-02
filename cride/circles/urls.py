"""Circles URLs."""

# Django
from django.urls import include, path

from rest_framework.routers import DefaultRouter

# Views
from cride.circles.views import CircleViewSet

router = DefaultRouter()
router.register(r'circles', CircleViewSet, basename='circle')

urlpatterns = [
    path('', include(router.urls))
]
