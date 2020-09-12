from rest_framework import serializers

from .models import Vehicle, Location


class LocationSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        vehicle = Vehicle.objects.get(
            pk=self.context['view'].kwargs['vehicle_pk']
        )
        validated_data['vehicle'] = vehicle
        return Location.objects.create(**validated_data)

    class Meta:
        model = Location
        fields = ['lat', 'lng', 'at']


class VehicleSerializer(serializers.ModelSerializer):
    steps = LocationSerializer(many=True, read_only=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'steps']
