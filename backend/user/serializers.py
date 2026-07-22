from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import Profile


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


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'name', 'celular', 'created_at', 'modified_at', 'status']
        read_only_fields = ['id', 'created_at', 'modified_at']
