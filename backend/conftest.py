import pytest

from cdr.models import Organization, Customer, Thing, Device
from user.models import Profile


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
        thing=thing, imsi='IMSI-001', imei='IMEI-001'
    )


@pytest.fixture
def user_data():
    return {'email': 'test@example.com', 'password': 'pass123'}


@pytest.fixture
def user(django_user_model, user_data):
    return django_user_model.objects.create_user(**user_data, is_staff=True)


@pytest.fixture
def profile(user, thing):
    return Profile.objects.create(user=user, name='Perfil Teste', thing=thing)


@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client


@pytest.fixture
def authenticated_client_with_profile(client, user, profile):
    client.force_login(user)
    return client
