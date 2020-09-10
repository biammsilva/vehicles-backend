from django.db import models


class Vehicle(models.Model):
    id = models.UUIDField(primary_key=True, serialize=True)


class Location(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    at = models.DateTimeField()
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE,
                                related_name='steps')
