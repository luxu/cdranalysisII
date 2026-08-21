from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

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

User = get_user_model()


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'orgid', 'orgname', 'created_at', 'modified_at', 'status']
        read_only_fields = ['id', 'created_at', 'modified_at']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id',
            'customerid',
            'customername',
            'organization',
            'created_at',
            'modified_at',
            'status',
        ]
        read_only_fields = ['id', 'created_at', 'modified_at']


class MnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mno
        fields = [
            'id',
            'mnoid',
            'mnoname',
            'organization',
            'created_at',
            'modified_at',
            'status',
        ]
        read_only_fields = ['id', 'created_at', 'modified_at']


class NetworkProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkProvider
        fields = [
            'id',
            'networkproviderid',
            'networkprovidername',
            'customer',
            'created_at',
            'modified_at',
            'status',
        ]
        read_only_fields = ['id', 'created_at', 'modified_at']


class PricePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricePlan
        fields = [
            'id',
            'priceplanid',
            'priceplanname',
            'customer',
            'created_at',
            'modified_at',
            'status',
        ]
        read_only_fields = ['id', 'created_at', 'modified_at']


class ThingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thing
        fields = [
            'id',
            'thingsgroupid',
            'thingsgroupname',
            'customer',
            'created_at',
            'modified_at',
            'status',
        ]
        read_only_fields = ['id', 'created_at', 'modified_at']


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = [
            'id',
            'thing',
            'iccid',
            'imsi',
            'imei',
            'created_at',
            'modified_at',
            'status',
        ]
        read_only_fields = ['id', 'created_at', 'modified_at']


class SessionSerializer(serializers.ModelSerializer):
    device_iccid = serializers.CharField(source='device.iccid', read_only=True)

    class Meta:
        model = Session
        fields = [
            'id',
            'device',
            'device_iccid',
            'sessionid',
            'sessioncreatetime',
            'realusage',
            'uom',
        ]
        read_only_fields = ['id', 'device_iccid']


class SessionListSerializer(serializers.ModelSerializer):
    iccid = serializers.CharField(source='device.iccid', read_only=True)
    thing_name = serializers.CharField(
        source='device.thing.thingsgroupname', read_only=True
    )

    class Meta:
        model = Session
        fields = [
            'id',
            'device',
            'iccid',
            'thing_name',
            'sessionid',
            'sessioncreatetime',
            'realusage',
            'uom',
        ]
        read_only_fields = ['id', 'iccid', 'thing_name']


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
    user_staff = serializers.BooleanField(source='user.is_staff', read_only=True)
    thing_name = serializers.CharField(source='thing.thingsgroupname', read_only=True)
    qtd_devices_com_sessao = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'user_email', 'user_staff', 'email', 'password',
            'name', 'celular', 'thing', 'thing_name',
            'qtd_devices_com_sessao'
        ]
        read_only_fields = ['id', 'user', 'qtd_devices_com_sessao', 'created_at', 'modified_at']

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
