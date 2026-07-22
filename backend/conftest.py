import pytest

from cdr.models import Organization, Customer, Thing, Device


@pytest.fixture
def organization():
    return Organization.objects.create(orgid='ORG-001', orgname='Org Teste')


@pytest.fixture
def customer(organization):
    return Customer.objects.create(
        customerid='CUST-001', customername='Cliente Teste', organization=organization
    )


@pytest.fixture
def thing(customer):
    return Thing.objects.create(
        thingsgroupid='THING-001', thingsgroupname='Grupo Teste', customer=customer
    )


@pytest.fixture
def device(thing):
    return Device.objects.create(
        thing=thing, imsi='IMSI-001', msisdn='999999999', imei='IMEI-001'
    )
