from rest_framework import serializers

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
            'msisdn',
            'imei',
            'created_at',
            'modified_at',
            'status',
        ]
        read_only_fields = ['id', 'created_at', 'modified_at']


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = [
            'id',
            'device',
            'sessionid',
            'sessioncreatetime',
            'realusage',
            'uom',
            'created_at',
            'modified_at',
            'status',
        ]
        read_only_fields = ['id', 'created_at', 'modified_at']
