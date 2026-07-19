from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from cdr.views import (
    CustomerViewSet,
    DeviceViewSet,
    MnoViewSet,
    NetworkProviderViewSet,
    OrganizationViewSet,
    PricePlanViewSet,
    SessionViewSet,
    ThingViewSet,
)
from user.views import LoginView, ProfileViewSet

router = DefaultRouter()
router.register('organizations', OrganizationViewSet)
router.register('customers', CustomerViewSet)
router.register('mnos', MnoViewSet)
router.register('networkproviders', NetworkProviderViewSet)
router.register('priceplans', PricePlanViewSet)
router.register('things', ThingViewSet)
router.register('devices', DeviceViewSet)
router.register('sessions', SessionViewSet)
router.register('profiles', ProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/', include(router.urls)),
]
