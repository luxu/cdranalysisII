from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CustomerViewSet,
    DeviceViewSet,
    LoginView,
    MnoViewSet,
    NetworkProviderViewSet,
    OrganizationViewSet,
    PricePlanViewSet,
    ProfileViewSet,
    SessionViewSet,
    ThingViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register('organizations', OrganizationViewSet)
router.register('customers', CustomerViewSet)
router.register('mnos', MnoViewSet)
router.register('networkproviders', NetworkProviderViewSet)
router.register('priceplans', PricePlanViewSet)
router.register('things', ThingViewSet)
router.register('devices', DeviceViewSet)
router.register('sessions', SessionViewSet)
router.register('users', UserViewSet)
router.register('profiles', ProfileViewSet)

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]
