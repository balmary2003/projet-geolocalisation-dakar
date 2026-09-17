from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers import serialize
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import PointOfInterest, Zone, Route, Restaurant, Avis
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D

def map_views(request):
    return render(request, 'map.html')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('map')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def restaurants_data(request):
    restaurants = Restaurant.objects.all()

    # Recherche par nom
    q = request.GET.get('q')
    if q:
        restaurants = restaurants.filter(nom__icontains=q)

    # Recherche par catégorie
    categorie = request.GET.get('categorie')
    if categorie:
        restaurants = restaurants.filter(categorie__iexact=categorie)

    # Recherche par proximité
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    rayon = request.GET.get('rayon', 5)  # rayon en km, 5 km par défaut

    fields = ['nom', 'description', 'adresse', 'telephone', 'horaires', 'categorie', 'image']

    if lat and lon:
        user_location = Point(float(lon), float(lat), srid=4326)
        restaurants = restaurants.filter(
            position__distance_lte=(user_location, D(km=float(rayon)))
        ).annotate(
            distance=Distance('position', user_location)
        ).order_by('distance')

        geojson = serialize(
            'geojson',
            restaurants,
            geometry_field='position',
            fields=fields
        )
        # Injecte la distance calculée dans chaque feature (serialize ne le fait pas nativement)
        import json
        data = json.loads(geojson)
        for feature, restaurant in zip(data['features'], restaurants):
            feature['properties']['distance_km'] = round(restaurant.distance.km, 2)
        return HttpResponse(json.dumps(data), content_type='application/json')

    geojson = serialize('geojson', restaurants, geometry_field='position', fields=fields)
    return HttpResponse(geojson, content_type='application/json')

def points_data(request):
    points = serialize('geojson', PointOfInterest.objects.all())
    return HttpResponse(points, content_type='application/json')


def zones_data(request):
    zones = serialize('geojson', Zone.objects.all())
    return HttpResponse(zones, content_type='application/json')


def routes_data(request):
    routes = serialize('geojson', Route.objects.all())
    return HttpResponse(routes, content_type='application/json')


@login_required
def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu_items = restaurant.menu_items.all()
    avis_list = restaurant.avis.all()
    mon_avis = avis_list.filter(utilisateur=request.user).first()
    return render(request, 'tracking/restaurant_detail.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'avis_list': avis_list,
        'mon_avis': mon_avis,
    })


@login_required
def ajouter_avis(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == 'POST':
        note = request.POST.get('note')
        commentaire = request.POST.get('commentaire')
        Avis.objects.update_or_create(
            restaurant=restaurant,
            utilisateur=request.user,
            defaults={'note': note, 'commentaire': commentaire}
        )
    return redirect('restaurant_detail', restaurant_id=restaurant_id)


@login_required
def supprimer_avis(request, restaurant_id):
    avis = get_object_or_404(Avis, restaurant_id=restaurant_id, utilisateur=request.user)
    if request.method == 'POST':
        avis.delete()
    return redirect('restaurant_detail', restaurant_id=restaurant_id)