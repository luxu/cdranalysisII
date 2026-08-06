import os
import tempfile
from api.services import import_cdr_from_file

from django.contrib.auth import get_user_model
from django.db.models import Count, FloatField, Max, Min, Q, Sum
from django.db.models.functions import Cast, TruncMonth
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from cdr.models import (
    Customer,
    Device,
    Mno,
    NetworkProvider,
    Organization,
    PricePlan,
    Session,
    Thing,
)
from user.models import Profile

from .serializers import (
    CustomerSerializer,
    DeviceSerializer,
    LoginSerializer,
    MnoSerializer,
    NetworkProviderSerializer,
    OrganizationSerializer,
    PricePlanSerializer,
    ProfileSerializer,
    SessionListSerializer,
    SessionSerializer,
    ThingSerializer,
    UserSerializer,
)

User = get_user_model()

class OwnerFilteredMixin:
    """Filtra queryset pelo thing do usuário logado. Admin vê tudo."""

    """
    Define qual campo do modelo no banco de dados será usado para filtrar. 
    Por padrão, ele vai buscar por thing_id.
    """
    owner_filter_field = 'thing_id'

    def _is_admin(self, user):
        if user.is_staff:
            return True
        return user.groups.filter(name__in=['Administrador', 'Manager']).exists()

    def _user_thing_id(self, user):
        try:
            return user.profile.thing_id
        except Exception:
            return None

    def _apply_owner_filter(self, qs):
        if not self._is_admin(self.request.user):
            thing_id = self._user_thing_id(self.request.user)
            if thing_id:
                # data = self.owner_filter_field: thing_id
                """
                A linha qs.filter(**{self.owner_filter_field: thing_id}) 
                equivale a fazer qs.filter(thing_id=thing_id)
                """
                qs = qs.filter(**{self.owner_filter_field: thing_id})
            else:
                qs = qs.none()
        return qs

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {
                'id': str(user.id),
                'email': user.email,
                'is_staff': user.is_staff,
                'groups': list(user.groups.values_list('name', flat=True)),
            },
        })


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
    page_size = 10
    page_size_query_param = 'page_size'  # <--- Habilita a leitura do 'page_size' da requisição
    queryset = Device.objects.select_related('thing').all()
    serializer_class = DeviceSerializer

    def get_queryset(self):
        qs = super().get_queryset()

        profile = getattr(self.request.user, 'profile', None)
        if profile and profile.thing_id:
            qs = qs.filter(thing=profile.thing)

        search = self.request.query_params.get('search')
        status = self.request.query_params.get('status')
        if search:
            qs = qs.filter(
                Q(iccid__icontains=search)
                | Q(imsi__icontains=search)
                | Q(imei__icontains=search)
            )
        if status is not None:
            status_bool = status.lower() in ('true', '1', 'ativo')
            qs = qs.filter(status=status_bool)
        return qs


class SessionViewSet(OwnerFilteredMixin, viewsets.ModelViewSet):
    page_size = 10
    page_size_query_param = 'page_size'  # <--- Habilita a leitura do 'page_size' da requisição
    queryset = Session.objects.select_related('device').all()
    serializer_class = SessionSerializer
    owner_filter_field = 'device__thing_id'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = self._apply_owner_filter(qs)

        start_date = self.request.query_params.get('start_date')
        if start_date:
            qs = qs.filter(sessioncreatetime__date__gte=start_date)

        end_date = self.request.query_params.get('end_date')
        if end_date:
            qs = qs.filter(sessioncreatetime__date__lte=end_date)

        device_id = self.request.query_params.get('device')
        if device_id:
            qs = qs.filter(device_id=device_id)

        device__thing = self.request.query_params.get('device__thing')
        if device__thing:
            qs = qs.filter(device__thing=device__thing)

        realusage_min = self.request.query_params.get('realusage_min')
        if realusage_min:
            qs = qs.filter(realusage__gte=realusage_min)

        realusage_max = self.request.query_params.get('realusage_max')
        if realusage_max:
            qs = qs.filter(realusage__lte=realusage_max)

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
        profile = getattr(self.request.user, 'profile', None)
        if profile and profile.thing and not self.request.user.is_staff:
            qs = qs.filter(device__thing=profile.thing)

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
                total_usage=Sum(Cast('realusage', output_field=FloatField())),
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
    def top_devices(self, request):
        qs = self.get_queryset()
        top = (
            qs
            .values('device', 'device__iccid', 'device__imsi')
            .annotate(
                total_bytes=Sum(Cast('realusage', output_field=FloatField())),
                session_count=Count('id')
            )
            .order_by('-total_bytes')[:10]
        )
        data = [
            {
                'device_id': str(t['device']),
                'iccid': t['device__iccid'],
                'imsi': t['device__imsi'],
                'total_bytes': float(t['total_bytes']) if t['total_bytes'] else 0,
                'session_count': t['session_count'],
            }
            for t in top
        ]
        return Response(data)

    @action(detail=False, methods=['get'], url_path='usage_by_month')
    def usage_by_month(self, request):
        qs = self.get_queryset()
        data = (
            qs
            .annotate(month=TruncMonth('sessioncreatetime'))
            .values('month')
            .annotate(
                total=Sum(Cast('realusage', output_field=FloatField())),
                qtd_sessoes=Count('id'),
            )
            .order_by('month')
        )

        result = [
            {
                'month': d['month'].strftime('%Y-%m') if d['month'] else None,
                'total': float(d['total']) if d['total'] else 0,
            }
            for d in data
        ]
        return Response(result)

    @action(detail=False, methods=['post'], url_path='import-cdr', permission_classes=[IsAdminUser])
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


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related('user', 'thing').all()
    serializer_class = ProfileSerializer

    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            profile = self.get_queryset().get(user=request.user)
        except Profile.DoesNotExist:
            return Response(
                {'error': 'Perfil não encontrado'},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def session_count(self, request, pk=None):
        profile = self.get_object()
        month = request.query_params.get('month')
        if not month:
            return Response(
                {'error': 'Parâmetro "month" é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        count = Session.objects.filter(
            device__thing=profile.thing,
            sessioncreatetime__month=month,
        ).count()
        return Response({
            'profile_id': str(profile.id),
            'month': int(month),
            'session_count': count,
        })

    @action(detail=True, methods=['get'])
    def sessions(self, request, pk=None):
        profile = self.get_object()
        sessions = Session.objects.filter(device__thing=profile.thing)
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def usage_by_month(self, request):
        profile = getattr(self.request.user, 'profile', None)
        if not profile or not profile.thing_id:
            return Response([])

        sessions = Session.objects.filter(device__thing=profile.thing)
        usage_by_month = sessions.values('sessioncreatetime__month').annotate(
            count=Count('id')
        ).order_by('sessioncreatetime__month')

        result = []
        for item in usage_by_month:
            result.append({
                'month': item['sessioncreatetime__month'],
                'count': item['count']
            })

        return Response(result)

    @action(detail=False, methods=['get'])
    def top_devices(self, request):
        profile = getattr(self.request.user, 'profile', None)
        if not profile or not profile.thing_id:
            return Response([])

        top_devices = Session.objects.filter(
            device__thing=profile.thing
        ).values(
            'device__id', 'device__thing__thingsgroupname'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:5]

        return Response(top_devices)
