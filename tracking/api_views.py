# tracking/api_views.py

from rest_framework import viewsets
from .models import PointOfInterest, Zone, Route
from .serializers import (
    PointOfInterestSerializer,
    ZoneSerializer,
    RouteSerializer
)


class PointOfInterestViewSet(viewsets.ModelViewSet):
    queryset = PointOfInterest.objects.all()
    serializer_class = PointOfInterestSerializer


class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer