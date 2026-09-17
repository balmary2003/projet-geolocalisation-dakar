from django.urls import path
from . import views

urlpatterns = [
    path('', views.map_views, name='home'),
    path('map/', views.map_views, name='map'),
    path('restaurants_data/', views.restaurants_data, name='restaurants_data'),
    path('points_data/', views.points_data, name='points_data'),
    path('zones_data/', views.zones_data, name='zones_data'),
    path('routes_data/', views.routes_data, name='routes_data'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('signup/', views.signup_view, name='signup'),
    path('restaurant/<int:restaurant_id>/avis/ajouter/', views.ajouter_avis, name='ajouter_avis'),
    path('restaurant/<int:restaurant_id>/avis/supprimer/', views.supprimer_avis, name='supprimer_avis'),
]