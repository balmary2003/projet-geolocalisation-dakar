from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from django.urls import reverse
from django.db import IntegrityError

from .models import Restaurant, MenuItem, Avis


class RestaurantModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            nom="Le Djembe",
            description="Cuisine sénégalaise",
            adresse="Rue 10, Dakar",
            telephone="+221 77 000 00 00",
            position=Point(-17.4859, 14.7249),
            categorie="Sénégalais"
        )

    def test_restaurant_str(self):
        self.assertEqual(str(self.restaurant), "Le Djembe")

    def test_restaurant_has_valid_position(self):
        self.assertAlmostEqual(self.restaurant.position.x, -17.4859, places=3)
        self.assertAlmostEqual(self.restaurant.position.y, 14.7249, places=3)


class MenuItemModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            nom="Le Djembe", description="Test", adresse="Dakar",
            telephone="000", position=Point(-17.48, 14.72)
        )
        self.plat = MenuItem.objects.create(
            restaurant=self.restaurant, nom="Thiéboudienne", prix=3500
        )

    def test_menu_item_cascade_delete(self):
        """Supprimer un restaurant doit supprimer ses plats associés."""
        self.assertEqual(MenuItem.objects.count(), 1)
        self.restaurant.delete()
        self.assertEqual(MenuItem.objects.count(), 0)


class AvisModelTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            nom="Le Djembe", description="Test", adresse="Dakar",
            telephone="000", position=Point(-17.48, 14.72)
        )
        self.user = User.objects.create_user(username="mary", password="testpass123")

    def test_avis_creation(self):
        avis = Avis.objects.create(restaurant=self.restaurant, utilisateur=self.user, note=5)
        self.assertEqual(avis.note, 5)

    def test_un_seul_avis_par_utilisateur_et_restaurant(self):
        """La contrainte unique_together doit empêcher un doublon d'avis."""
        Avis.objects.create(restaurant=self.restaurant, utilisateur=self.user, note=4)
        with self.assertRaises(IntegrityError):
            Avis.objects.create(restaurant=self.restaurant, utilisateur=self.user, note=2)


class RestaurantsDataViewTest(TestCase):
    def setUp(self):
        Restaurant.objects.create(
            nom="Le Djembe", description="Test", adresse="Dakar",
            telephone="000", position=Point(-17.48, 14.72), categorie="Sénégalais"
        )
        Restaurant.objects.create(
            nom="Mermoz Pizza", description="Test", adresse="Dakar",
            telephone="000", position=Point(-17.46, 14.70), categorie="Italien"
        )

    def test_restaurants_data_returns_geojson(self):
        response = self.client.get(reverse('restaurants_data'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['type'], 'FeatureCollection')
        self.assertEqual(len(data['features']), 2)

    def test_recherche_par_nom(self):
        response = self.client.get(reverse('restaurants_data'), {'q': 'djembe'})
        data = response.json()
        self.assertEqual(len(data['features']), 1)
        self.assertEqual(data['features'][0]['properties']['nom'], "Le Djembe")

    def test_recherche_par_categorie(self):
        response = self.client.get(reverse('restaurants_data'), {'categorie': 'Italien'})
        data = response.json()
        self.assertEqual(len(data['features']), 1)
        self.assertEqual(data['features'][0]['properties']['nom'], "Mermoz Pizza")


class RestaurantDetailViewTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            nom="Le Djembe", description="Test", adresse="Dakar",
            telephone="000", position=Point(-17.48, 14.72)
        )
        self.user = User.objects.create_user(username="mary", password="testpass123")

    def test_acces_refuse_si_non_connecte(self):
        """Un utilisateur non authentifié doit être redirigé vers la connexion."""
        response = self.client.get(reverse('restaurant_detail', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_acces_autorise_si_connecte(self):
        self.client.login(username="mary", password="testpass123")
        response = self.client.get(reverse('restaurant_detail', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Le Djembe")


class AvisViewTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            nom="Le Djembe", description="Test", adresse="Dakar",
            telephone="000", position=Point(-17.48, 14.72)
        )
        self.user = User.objects.create_user(username="mary", password="testpass123")
        self.autre_user = User.objects.create_user(username="alex", password="testpass123")
        self.client.login(username="mary", password="testpass123")

    def test_ajouter_avis_cree_un_avis(self):
        self.client.post(reverse('ajouter_avis', args=[self.restaurant.id]), {
            'note': 5, 'commentaire': 'Excellent restaurant'
        })
        self.assertEqual(Avis.objects.count(), 1)

    def test_modifier_avis_ne_cree_pas_de_doublon(self):
        """Poster deux fois un avis doit mettre à jour, pas dupliquer."""
        url = reverse('ajouter_avis', args=[self.restaurant.id])
        self.client.post(url, {'note': 3, 'commentaire': 'Correct'})
        self.client.post(url, {'note': 5, 'commentaire': 'Finalement excellent'})
        self.assertEqual(Avis.objects.count(), 1)
        self.assertEqual(Avis.objects.first().note, 5)

    def test_impossible_de_supprimer_avis_dautrui(self):
        """Un utilisateur ne peut pas supprimer l'avis d'un autre utilisateur."""
        Avis.objects.create(restaurant=self.restaurant, utilisateur=self.autre_user, note=4)
        response = self.client.post(reverse('supprimer_avis', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Avis.objects.count(), 1)