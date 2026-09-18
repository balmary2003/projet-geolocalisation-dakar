from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from tracking.models import Restaurant, MenuItem


class Command(BaseCommand):
    help = "Ajoute les restaurants et menus de démonstration"

    def handle(self, *args, **options):
        if Restaurant.objects.exists():
            self.stdout.write("Des restaurants existent déjà, aucune donnée ajoutée.")
            return

        data = [
            ("Le Djembe", "Découvrez la cuisine sénégalaise", "Rue 10, Dakar", "+221 77 000 00 00", "10h - 22h", "Sénégalais", -17.48589977041962, 14.724886547902775),
            ("Chez Fatou", "Cuisine locale et grillades", "Ouakam, Dakar", "+221 77 111 11 11", "9h - 23h", "Sénégalais", -17.4900, 14.7250),
            ("La Terrasse Almadies", "Spécialités fruits de mer face à l'océan", "Almadies, Dakar", "+221 77 222 22 22", "11h - 23h", "Fruits de mer", -17.5142, 14.7444),
            ("Le Baobab Gourmand", "Restaurant gastronomique sénégalais", "Plateau, Dakar", "+221 77 333 33 33", "12h - 22h", "Gastronomique", -17.4381, 14.6708),
            ("Dibiterie Yoff", "Grillades traditionnelles", "Yoff, Dakar", "+221 77 444 44 44", "17h - 1h", "Grillades", -17.4677, 14.7469),
            ("Le Point E Café", "Café et petit-déjeuner", "Point E, Dakar", "+221 77 555 55 55", "7h - 20h", "Café", -17.4600, 14.7000),
            ("Saveurs de Ngor", "Cuisine sénégalaise authentique", "Ngor, Dakar", "+221 77 666 66 66", "10h - 22h", "Sénégalais", -17.5158, 14.7522),
            ("Mermoz Pizza", "Pizzas et pâtes italiennes", "Mermoz, Dakar", "+221 77 777 77 77", "11h - 23h", "Italien", -17.4661, 14.7089),
            ("Fann Food Truck", "Street food et snacks", "Fann, Dakar", "+221 77 888 88 88", "12h - 21h", "Street food", -17.4544, 14.6889),
        ]

        menus = {
            "Le Djembe": [("Thiéboudienne", "Riz au poisson et légumes", 3500), ("Yassa Poulet", "Poulet mariné au citron", 3000), ("Bissap", "Boisson à l'hibiscus", 500)],
            "Chez Fatou": [("Thiéboudienne", "Riz au poisson et légumes", 3500), ("Yassa Poulet", "Poulet mariné au citron et oignons", 3000), ("Bissap", "Boisson à l'hibiscus", 500)],
            "La Terrasse Almadies": [("Plateau de fruits de mer", "Crevettes, langoustes, poissons grillés", 12000), ("Poisson braisé", "Poisson entier grillé", 6000), ("Jus de bouye", "Jus de fruit de baobab", 1000)],
            "Le Baobab Gourmand": [("Mafé", "Ragoût de viande à la pâte d'arachide", 4000), ("Thiou", "Ragoût de légumes et viande", 3800), ("Bantaba spécial", "Assortiment de spécialités locales", 7500)],
            "Dibiterie Yoff": [("Dibi mouton", "Viande de mouton grillée", 4500), ("Dibi bœuf", "Viande de bœuf grillée", 4000), ("Alloco", "Bananes plantains frites", 1500)],
            "Le Point E Café": [("Petit-déjeuner complet", "Café, pain, omelette, confiture", 2500), ("Croissant", "Viennoiserie fraîche", 700), ("Café Touba", "Café traditionnel épicé", 500)],
            "Saveurs de Ngor": [("Thiéboudienne rouge", "Riz au poisson, sauce tomate", 3500), ("Soupe kandia", "Sauce gombo au poisson fumé", 3200), ("Bissap", "Boisson à l'hibiscus", 500)],
            "Mermoz Pizza": [("Pizza Margherita", "Tomate, mozzarella, basilic", 4500), ("Pizza 4 fromages", "Mozzarella, gorgonzola, chèvre, parmesan", 5500), ("Tiramisu", "Dessert italien classique", 2000)],
            "Fann Food Truck": [("Chawarma poulet", "Sandwich garni au poulet", 2000), ("Frites maison", "Pommes de terre frites", 1000), ("Jus de gingembre", "Boisson artisanale", 800)],
        }

        for nom, desc, adresse, tel, horaires, cat, lon, lat in data:
            restaurant = Restaurant.objects.create(
                nom=nom, description=desc, adresse=adresse, telephone=tel,
                position=Point(lon, lat), horaires=horaires, categorie=cat
            )
            for plat_nom, plat_desc, prix in menus.get(nom, []):
                MenuItem.objects.create(restaurant=restaurant, nom=plat_nom, description=plat_desc, prix=prix)

        self.stdout.write(self.style.SUCCESS(f"{len(data)} restaurants ajoutés avec leurs menus."))