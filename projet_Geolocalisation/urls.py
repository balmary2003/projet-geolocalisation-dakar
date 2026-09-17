"""
URL configuration for projet_Geolocalisation project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from tracking.api_views import (
    PointOfInterestViewSet,
    ZoneViewSet,
    RouteViewSet
)

router = routers.DefaultRouter()
router.register(r'points', PointOfInterestViewSet)
router.register(r'zones', ZoneViewSet)
router.register(r'routes', RouteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tracking/', include('tracking.urls')),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)