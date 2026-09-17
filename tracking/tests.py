from django.test import TestCase
from django.contrib.gis.geos import Point, Polygon, LineString
from django.test import TestCase

from .models import PointOfInterest, Zone, Route


class GISModelAdmintest(TestCase):

    def setUp(self):
         # Point d’intérêt à Dakar
        PointOfInterest.objects.create(
            name="Monument de la Renaissance",
            location=Point(-17.4946, 14.7368, srid=4326)
        )


        # Zone représentant une partie de Dakar
        Zone.objects.create(
            name="Dakar Centre",
            area=Polygon((
                (-17.6, 14.6),
                (-17.3, 14.6),
                (-17.3, 14.9),
                (-17.6, 14.9),
                (-17.6, 14.6)
            ), srid=4326)
        )

        # Route dans Dakar
        Route.objects.create(
            name="Route Dakar",
            path=LineString(
                (-17.5, 14.7),
                (-17.45, 14.75),
                (-17.4, 14.72),
                srid=4326
            )
        )

    def test_point_of_interest_creation(self):

        monument = PointOfInterest.objects.get(
            name="Monument de la Renaissance"
        )

        self.assertEqual(monument.location.x, -17.4946)
        self.assertEqual(monument.location.y, 14.7368)

    def test_zone_area(self):

        dakar = Zone.objects.get(name="Dakar Centre")

        self.assertIsInstance(dakar.area, Polygon)

    def test_route_path(self):

        route = Route.objects.get(name="Route Dakar")

        self.assertIsInstance(route.path, LineString)

        self.assertEqual(len(route.path.coords), 3)

    def test_spatial_query(self):

        # Zone couvrant Dakar
        dakar_area = Polygon((
            (-17.6, 14.6),
            (-17.3, 14.6),
            (-17.3, 14.9),
            (-17.6, 14.9),
            (-17.6, 14.6)
        ), srid=4326)

        Zone.objects.create(
            name="Grande Zone Dakar",
            area=dakar_area
        )

        monument = PointOfInterest.objects.get(
            name="Monument de la Renaissance"
        )

        points_in_dakar = PointOfInterest.objects.filter(
            location__within=dakar_area
        )

        self.assertIn(monument, points_in_dakar)