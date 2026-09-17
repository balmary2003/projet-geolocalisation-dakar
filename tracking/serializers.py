
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import PointOfInterest, Zone, Route

class PointOfInterestSerializer(GeoFeatureModelSerializer):
  class Meta:
    model = PointOfInterest
    geo_field = "location"
    fields = ("id", "name", "description", "location")
    
class ZoneSerializer(GeoFeatureModelSerializer):
  class Meta:
   model = Zone
   geo_field = "area"
   fields = ("id", "name", "area")
   
class RouteSerializer(GeoFeatureModelSerializer):
  class Meta:
   model = Route
   geo_field = "path"
   fields = ("id", "name", "path")