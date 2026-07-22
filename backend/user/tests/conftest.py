import pytest
from pytest_django.fixtures import django_user_model


@pytest.fixture
def user_data():
    return {'email': 'test@example.com', 'password': 'pass123'}


@pytest.fixture
def user(django_user_model, user_data):
    return django_user_model.objects.create_user(**user_data)


@pytest.fixture
def authenticated_client(client, user):
    client.force_login(user)
    return client
