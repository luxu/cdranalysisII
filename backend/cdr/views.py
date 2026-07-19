from rest_framework import viewsets

from .models import (
    Customer,
    Device,
    Mno,
    NetworkProvider,
    Organization,
    PricePlan,
    Session,
    Thing,
)
from .serializers import (
    CustomerSerializer,
    DeviceSerializer,
    MnoSerializer,
    NetworkProviderSerializer,
    OrganizationSerializer,
    PricePlanSerializer,
    SessionSerializer,
    ThingSerializer,
)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.select_related('organization').all()
    serializer_class = CustomerSerializer


class MnoViewSet(viewsets.ModelViewSet):
    queryset = Mno.objects.select_related('organization').all()
    serializer_class = MnoSerializer


class NetworkProviderViewSet(viewsets.ModelViewSet):
    queryset = NetworkProvider.objects.select_related('customer').all()
    serializer_class = NetworkProviderSerializer


class PricePlanViewSet(viewsets.ModelViewSet):
    queryset = PricePlan.objects.select_related('customer').all()
    serializer_class = PricePlanSerializer


class ThingViewSet(viewsets.ModelViewSet):
    queryset = Thing.objects.select_related('customer').all()
    serializer_class = ThingSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.select_related('thing').all()
    serializer_class = DeviceSerializer


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.select_related('device').all()
    serializer_class = SessionSerializer
