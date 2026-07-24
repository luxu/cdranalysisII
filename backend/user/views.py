from django.contrib.auth import get_user_model

from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from cdr.models import Session
from cdr.serializers import SessionSerializer

from .models import Profile
from .serializers import LoginSerializer, ProfileSerializer, UserSerializer

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
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({
                'user': str(request.user.id),
                'thing': None,
                'thing_name': None,
                'name': request.user.email,
                'is_staff': request.user.is_staff,
            })

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
