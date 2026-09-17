from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from leaflet.admin import LeafletGeoAdmin
from .models import PointOfInterest, Zone, Route, Restaurant, MenuItem, Avis


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1


@admin.register(Restaurant)
class RestaurantAdmin(GISModelAdmin):
    list_display = ('nom', 'adresse', 'categorie', 'telephone', 'date_ajout')
    list_filter = ('categorie',)
    search_fields = ('nom', 'adresse')
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('nom', 'restaurant', 'prix')
    list_filter = ('restaurant',)
    search_fields = ('nom',)


class DakarGISAdmin(LeafletGeoAdmin):
    settings_overrides = {
        'DEFAULT_CENTER': (14.6928, -17.4441),
        'DEFAULT_ZOOM': 12,
    }
    map_width = 800
    map_height = 500


@admin.register(PointOfInterest)
class PointOfInterestAdmin(DakarGISAdmin):
    list_display = ('name', 'location')


@admin.register(Zone)
class ZoneAdmin(DakarGISAdmin):
    list_display = ('name', 'area')


@admin.register(Route)
class RouteAdmin(DakarGISAdmin):
    list_display = ('name', 'path')
   
@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'utilisateur', 'note', 'date_creation')
    list_filter = ('note', 'restaurant')