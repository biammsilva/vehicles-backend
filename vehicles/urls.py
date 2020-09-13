from django.urls import include
from rest_framework_nested import routers
from rest_framework.urls import url

from .views import VehicleViewSet, LocationViewSet

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'vehicles', VehicleViewSet)

vehicles_router = routers.NestedSimpleRouter(router, r'vehicles',
                                             lookup='vehicle')

vehicles_router.register(
    'locations',
    LocationViewSet,
)

urlpatterns = [
    url(r'^', include(router.urls)),
    url('^', include(vehicles_router.urls)),
]
