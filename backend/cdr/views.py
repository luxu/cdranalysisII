from django.db.models import Q, Sum
from django.db.models.functions import TruncMonth

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=False, methods=['get'])
    def usage_by_month(self, request):
        qs = self.filter_queryset(self.get_queryset())
        months = (
            qs
            .annotate(month=TruncMonth('sessioncreatetime'))
            .values('month')
            .annotate(total=Sum('realusage'))
            .order_by('month')
        )
        data = [
            {
                'month': m['month'].strftime('%Y-%m') if m['month'] else None,
                'total': float(m['total']) if m['total'] else 0,
            }
            for m in months
        ]
        return Response(data)

    @action(detail=False, methods=['get'])
    def top_devices(self, request):
        qs = self.filter_queryset(self.get_queryset())
        top = (
            qs
            .values('device', 'device__iccid', 'device__imsi', 'device__msisdn')
            .annotate(total=Sum('realusage'))
            .order_by('-total')[:10]
        )
        data = [
            {
                'device_id': str(t['device']),
                'iccid': t['device__iccid'],
                'imsi': t['device__imsi'],
                'msisdn': t['device__msisdn'],
                'total_bytes': float(t['total']) if t['total'] else 0,
            }
            for t in top
        ]
        return Response(data)
