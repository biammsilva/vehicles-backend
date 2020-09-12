from django.test import TestCase
from rest_framework.exceptions import ValidationError

from .models import Location, Vehicle


class VehicleLocationsModelTestCase(TestCase):
    def setUp(self):
        vehicle_1 = Vehicle.objects.create(
            id='5084decc-f45d-11ea-adc1-0242ac120002'
        )
        vehicle_2 = Vehicle.objects.create(
            id='5ee32186-f45d-11ea-adc1-0242ac120002'
        )
        Location.objects.create(
            at='2020-09-11T18:40:55Z', lat=52.53, lng=13.40, vehicle=vehicle_1
        )
        Location.objects.create(
            at='2020-09-11T18:42:55Z', lat=52.53, lng=13.40, vehicle=vehicle_1
        )
        Location.objects.create(
            at='2020-09-11T18:44:55Z', lat=52.53, lng=13.40, vehicle=vehicle_1
        )
        Location.objects.create(
            at='2020-09-11T18:46:55Z', lat=52.53, lng=13.40, vehicle=vehicle_1
        )
        Location.objects.create(
            at='2020-09-11T18:40:55Z', lat=52.53, lng=13.40, vehicle=vehicle_2
        )

    def test_location_added_to_vehicle(self):
        """ Test if the locations was correctly added to vehicles """
        vehicle_1 = Vehicle.objects.get(
            id='5084decc-f45d-11ea-adc1-0242ac120002'
        )
        vehicle_2 = Vehicle.objects.get(
            id='5ee32186-f45d-11ea-adc1-0242ac120002'
        )
        locations_vehicle_1 = vehicle_1.steps.all()
        locations_vehicle_2 = vehicle_2.steps.all()
        self.assertEqual(len(locations_vehicle_1), 4)
        self.assertEqual(len(locations_vehicle_2), 1)

    def test_location_is_not_on_city_boundaries(self):
        vehicle_1 = Vehicle.objects.get(
            id='5084decc-f45d-11ea-adc1-0242ac120002'
        )
        location = Location(
            at='2020-09-11T18:46:55Z', lat=10, lng=21, vehicle=vehicle_1
        )
        self.assertFalse(location.is_on_city_boundaries())

    def test_location_is_on_city_boundaries(self):
        vehicle_1 = Vehicle.objects.get(
            id='5084decc-f45d-11ea-adc1-0242ac120002'
        )
        location = Location(
            at='2020-09-11T18:46:55Z', lat=52.52, lng=13.41, vehicle=vehicle_1
        )
        self.assertTrue(location.is_on_city_boundaries())

    def test_raise_create_location_is_not_on_city_boundaries(self):
        vehicle_1 = Vehicle.objects.get(
            id='5084decc-f45d-11ea-adc1-0242ac120002'
        )
        with self.assertRaises(ValidationError):
            Location.objects.create(
                at='2020-09-11T18:40:55Z',
                lat=55.53,
                lng=13.40,
                vehicle=vehicle_1
            )
