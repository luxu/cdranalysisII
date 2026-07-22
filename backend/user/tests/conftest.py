import pytest


@pytest.fixture
def profile(user, thing):
    from user.models import Profile
    return Profile.objects.create(user=user, name='Perfil Teste', thing=thing)
