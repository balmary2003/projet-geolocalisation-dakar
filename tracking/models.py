from django.contrib.gis.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    position = models.PointField(geography=True)  # coordonnées GPS (lat/lon en mètres réels)
    horaires = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='restaurants/', blank=True, null=True)
    categorie = models.CharField(max_length=100, blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"


class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='menu_items', on_delete=models.CASCADE)
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)

    def __str__(self):
        return f"{self.nom} - {self.restaurant.nom}"

    class Meta:
        verbose_name = "Plat"
        verbose_name_plural = "Menu"


class PointOfInterest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    location = models.PointField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Zone(models.Model):
    name = models.CharField(max_length=100)
    area = models.PolygonField()

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=100)
    path = models.LineStringField()

    def __str__(self):
        return self.name


class Avis(models.Model):
    NOTE_CHOICES = [(i, str(i)) for i in range(1, 6)]

    restaurant = models.ForeignKey(Restaurant, related_name='avis', on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.IntegerField(choices=NOTE_CHOICES)
    commentaire = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.restaurant.nom} - {self.note}/5"

    class Meta:
        verbose_name = "Avis"
        verbose_name_plural = "Avis"
        unique_together = ('restaurant', 'utilisateur')  # un seul avis par utilisateur et par restaurant
        ordering = ['-date_creation']