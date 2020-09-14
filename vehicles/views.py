from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response

from .models import Vehicle, Location
from .serializers import VehicleSerializer, LocationSerializer


class VehicleViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    API endpoint that allows vehicles to be added, viewed or edited.

    list:
    Return a list of the vehicles that have any location.
    Parameter 'all': If 'true' return all the vehicles

    retrieve:
    Return the vehicle if its not deleted. Should return\
        the vehicle that has no locations too.

    create:
    Create a vehicle

    destroy:
    Soft deletes a vehicle

    """
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def get_queryset(self):
        if bool(self.request.query_params.get('all')) or\
           self.kwargs.get('pk'):
            return self.queryset
        return self.queryset.exclude(steps=None)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(None, status=status.HTTP_204_NO_CONTENT,
                        headers=headers)


class LocationViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    """
    API endpoint that allows locations to be added, viewed or edited.

    list:
    Return a list of the locations of the vehicle.

    create:
    Adds a location to the vehicle

    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        return Location.objects.filter(
            vehicle=self.kwargs['vehicle_pk']
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(None, status=status.HTTP_204_NO_CONTENT,
                        headers=headers)
