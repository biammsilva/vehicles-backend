from django.db import models
from geopy.distance import distance
from rest_framework.exceptions import ValidationError


DOOR_2_DOOR_LATLONG = (52.53, 13.403)


class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, serialize=True)


class LocationOrderedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('at')


class Location(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    at = models.DateTimeField()
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE,
                                related_name='steps')
    objects = LocationOrderedManager()

    def is_on_city_boundaries(self):
        calculated_distance = distance(
            (self.lat, self.lng),
            DOOR_2_DOOR_LATLONG
        ).km
        return calculated_distance <= 3.5

    def save(self, *args, **kwargs):
        if self.is_on_city_boundaries():
            return super().save()
        raise ValidationError('Location out of the city boundaries')
