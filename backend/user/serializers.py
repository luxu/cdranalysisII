from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Profile

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get('request'),
            username=attrs['email'],
            password=attrs['password'],
        )
        if not user:
            raise serializers.ValidationError('Credenciais inválidas')
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_staff']


class ProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    thing_name = serializers.CharField(source='thing.thingsgroupname', read_only=True)
    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'user_email', 'email', 'password',
            'name', 'celular', 'thing', 'thing_name',
            'status', 'created_at', 'modified_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'modified_at']

    def validate(self, attrs):
        if not self.instance:
            email = attrs.get('email')
            if not email:
                raise serializers.ValidationError({'email': 'Email é obrigatório'})
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError({'email': 'Email já cadastrado'})
            attrs.setdefault('password', '123mudar')
        else:
            attrs.pop('email', None)
            attrs.pop('password', None)
        return attrs

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password', '123mudar')
        user = User.objects.create_user(email=email, password=password)
        validated_data.pop('user', None)
        return Profile.objects.create(user=user, **validated_data)
