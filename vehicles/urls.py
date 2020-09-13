from django.urls import include
from rest_framework_nested import routers
from rest_framework.urls import url

from .views import VehicleViewSet, LocationViewSet

router = routers.SimpleRouter()

router.register('', VehicleViewSet)

vehicles_router = routers.NestedSimpleRouter(router, '', lookup='vehicle')

vehicles_router.register(
    'locations',
    LocationViewSet,
)

urlpatterns = [
    url('', include(router.urls)),
    url('', include(vehicles_router.urls)),
]
