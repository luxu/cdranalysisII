from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

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
    SessionSerializer,
    ThingSerializer,
    UserSerializer,
)

User = get_user_model()


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
