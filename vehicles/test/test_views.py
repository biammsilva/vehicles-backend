from django.test import TestCase
from rest_framework.test import APIClient

from ..models import Location, Vehicle


class BaseViewTest(TestCase):
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
            at='2020-09-11T18:40:55Z', lat=52.53, lng=13.40, vehicle=vehicle_2
        )
        self.client = APIClient()


class VehicleViewTestCase(BaseViewTest):

    def test_success_get_all_vehicles(self):
        response = self.client.get('/vehicles/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            {
                "id": "5084decc-f45d-11ea-adc1-0242ac120002",
                "steps": [
                    {
                        "lat": 52.53,
                        "lng": 13.40,
                        "at": "2020-09-11T18:40:55Z"
                    },
                    {
                        "lat": 52.53,
                        "lng": 13.40,
                        "at": "2020-09-11T18:42:55Z"
                    }
                ]
            }, {
                "id": "5ee32186-f45d-11ea-adc1-0242ac120002",
                "steps": [
                    {
                        "lat": 52.53,
                        "lng": 13.40,
                        "at": "2020-09-11T18:40:55Z"
                    }
                ]
            }
        ])

    def test_success_get_one_vehicle(self):
        response = self.client.get(
            '/vehicles/5ee32186-f45d-11ea-adc1-0242ac120002/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "id": "5ee32186-f45d-11ea-adc1-0242ac120002",
            "steps": [
                {
                    "lat": 52.53,
                    "lng": 13.40,
                    "at": "2020-09-11T18:40:55Z"
                }
            ]
        })

    def test_success_post_new_vehicle(self):
        response = self.client.post('/vehicles/', {
            'id': '8412e8a2-f52e-11ea-adc1-0242ac120002'
        })
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, None)


class LocationViewTestCase(BaseViewTest):

    def test_success_get_all_locations_from_a_vehicle(self):
        response = self.client.get(
            '/vehicles/5084decc-f45d-11ea-adc1-0242ac120002/locations/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [
            {
                "lat": 52.53,
                "lng": 13.40,
                "at": "2020-09-11T18:40:55Z"
            },
            {
                "lat": 52.53,
                "lng": 13.40,
                "at": "2020-09-11T18:42:55Z"
            }
        ])

    def test_success_create_location_on_city_boundaries(self):
        response = self.client.post(
            '/vehicles/5084decc-f45d-11ea-adc1-0242ac120002/locations/', {
                "lat": 52.53,
                "lng": 13.41,
                "at": "2017-09-01T12:10:00Z"
            }
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, None)

    def test_success_create_location_out_of_city_boundaries(self):
        response = self.client.post(
            '/vehicles/5084decc-f45d-11ea-adc1-0242ac120002/locations/', {
                "lat": 52.53,
                "lng": 13.49,
                "at": "2017-09-01T12:10:00Z"
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, [
            "Location out of the city boundaries"
        ])
