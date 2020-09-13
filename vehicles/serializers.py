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
    last_lat = serializers.SerializerMethodField(read_only=True)
    last_lng = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'last_lat', 'last_lng']

    def get_last_lat(self, obj):
        if obj.steps.all():
            last_location = Location.objects.filter(
                vehicle=obj.id
            ).order_by('-at')[:1][0]
            return last_location.lat
        return None

    def get_last_lng(self, obj):
        if obj.steps.all():
            last_location = Location.objects.filter(
                vehicle=obj.id
            ).order_by('-at')[:1][0]
            return last_location.lng
        return None
