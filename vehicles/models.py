from django.db import models
from geopy.distance import distance
from geopy.geocoders import Nominatim
from rest_framework.exceptions import ValidationError


DOOR_2_DOOR_LATLONG = (52.53, 13.403)


class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, serialize=True)


class LocationOrderedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_same_street=False
        ).order_by('at')


class Location(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    at = models.DateTimeField()
    is_same_street = models.BooleanField(default=False)
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE,
                                related_name='steps')
    objects = LocationOrderedManager()

    def is_on_city_boundaries(self):
        calculated_distance = distance(
            (self.lat, self.lng),
            DOOR_2_DOOR_LATLONG
        ).km
        return calculated_distance <= 3.5

    def is_on_same_street(self):
        geolocator = Nominatim(user_agent='vehicles-location')
        location = geolocator.reverse((self.lat, self.lng))
        if self.vehicle.steps.all():
            last_lat_lng = self.vehicle.steps.all().order_by('-at')[0]
            last_location = geolocator.reverse(
                (last_lat_lng.lat, last_lat_lng.lng)
            )
            if last_location.raw['address']['road']\
               == location.raw['address']['road']:
                return True
        return False

    def save(self, *args, **kwargs):
        if self.is_on_city_boundaries():
            self.is_same_street = self.is_on_same_street()
            return super().save(*args, **kwargs)
        raise ValidationError('Location out of the city boundaries')
