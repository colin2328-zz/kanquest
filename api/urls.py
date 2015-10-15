from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import PlayerViewSet

router = DefaultRouter()
router.register(r'players', PlayerViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
