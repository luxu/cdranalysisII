import os
import tempfile

from django.db.models import Q, Sum, Count, Min, Max
from django.db.models.functions import TruncMonth

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
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
    SessionListSerializer,
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
        if thing:
            qs = qs.filter(thing_id=thing)
        if search:
            qs = qs.filter(
                Q(iccid__icontains=search)
                | Q(imsi__icontains=search)
                | Q(imei__icontains=search)
            )
        return qs


class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.select_related('device').all()
    serializer_class = SessionSerializer

    def get_queryset(self):
        qs = Session.objects.select_related('device__thing').all()
        device__thing = self.request.query_params.get('device__thing')
        if device__thing:
            qs = qs.filter(device__thing_id=device__thing)
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(
                Q(sessionid__icontains=search)
                | Q(device__imsi__icontains=search)
                | Q(device__iccid__icontains=search)
                | Q(device__thing__thingsgroupname__icontains=search)
            )
        start_date = self.request.query_params.get('start_date')
        if start_date:
            qs = qs.filter(sessioncreatetime__date__gte=start_date)
        end_date = self.request.query_params.get('end_date')
        if end_date:
            qs = qs.filter(sessioncreatetime__date__lte=end_date)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return SessionListSerializer
        return SessionSerializer

    @action(detail=False, methods=['get'])
    def date_range(self, request):
        result = Session.objects.aggregate(
            min_date=Min('sessioncreatetime__date'),
            max_date=Max('sessioncreatetime__date'),
        )
        return Response({
            'min_date': result['min_date'].isoformat() if result['min_date'] else None,
            'max_date': result['max_date'].isoformat() if result['max_date'] else None,
        })

    @action(detail=False, methods=['get'])
    def summary_by_thing(self, request):
        qs = Session.objects.select_related('device__thing')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date:
            qs = qs.filter(sessioncreatetime__date__gte=start_date)
        if end_date:
            qs = qs.filter(sessioncreatetime__date__lte=end_date)
        data = (
            qs
            .values(
                'device__thing__id',
                'device__thing__thingsgroupname',
            )
            .annotate(
                device_count=Count('device', distinct=True),
                total_usage=Sum('realusage'),
            )
            .order_by('device__thing__thingsgroupname')
        )
        result = [
            {
                'thing_id': str(d['device__thing__id']),
                'thing_name': d['device__thing__thingsgroupname'],
                'device_count': d['device_count'],
                'total_usage': float(d['total_usage']) if d['total_usage'] else 0,
            }
            for d in data
        ]
        return Response(result)

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
            .values('device', 'device__iccid', 'device__imsi')
            .annotate(total=Sum('realusage'), session_count=Count('id'))
            .order_by('-total')[:10]
        )
        data = [
            {
                'device_id': str(t['device']),
                'iccid': t['device__iccid'],
                'imsi': t['device__imsi'],
                'total_bytes': float(t['total']) if t['total'] else 0,
                'session_count': t['session_count'],
            }
            for t in top
        ]
        return Response(data)

    @action(
        detail=False,
        methods=['post'],
        url_path='import-cdr',
        permission_classes=[IsAdminUser],
    )
    def import_cdr(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response(
                {'error': 'Nenhum arquivo enviado'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not file.name.endswith(('.xlsx', '.xls', '.csv')):
            return Response(
                {'error': 'Formato inválido. Use .xlsx, .xls ou .csv'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tmp_path = None
        try:
            ext = os.path.splitext(file.name)[1]
            with tempfile.NamedTemporaryFile(
                suffix=ext, delete=False
            ) as tmp:
                for chunk in file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            from cdr.services import import_cdr_from_file

            stats = import_cdr_from_file(tmp_path)
            return Response(stats)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
