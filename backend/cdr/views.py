from django.db.models import Q

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

    def get_queryset(self):
        qs = super().get_queryset()
        thing = self.request.query_params.get('thing')
        search = self.request.query_params.get('search')
        status = self.request.query_params.get('status')
        if thing:
            qs = qs.filter(thing_id=thing)
        if search:
            qs = qs.filter(
                Q(iccid__icontains=search)
                | Q(imsi__icontains=search)
                | Q(msisdn__icontains=search)
                | Q(imei__icontains=search)
            )
        if status is not None:
            status_bool = status.lower() in ('true', '1', 'ativo')
            qs = qs.filter(status=status_bool)
        return qs


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.select_related('device').all()
    serializer_class = SessionSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        device__thing = self.request.query_params.get('device__thing')
        if device__thing:
            qs = qs.filter(device__thing_id=device__thing)
        return qs
