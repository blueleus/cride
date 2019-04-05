"""Circles URLs."""

# Django
from django.urls import include, path

from rest_framework.routers import DefaultRouter

# Views
from cride.circles.views import CircleViewSet
from .views import memberships as membership_views

router = DefaultRouter()
router.register(r'circles', CircleViewSet, basename='circle')
router.register(
    r'circles/(?P<slug_name>[-a-zA-Z0-9_]+)/members',
    membership_views.MembershipViewSet,
    basename='membership'
)

urlpatterns = [
    path('', include(router.urls))
]
