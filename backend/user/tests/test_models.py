import pytest
from django.contrib.auth import get_user_model

from datetime import datetime

from django.utils.timezone import make_aware

from cdr.models import Session

from user.models import Profile

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    def test_create_user(self):
        user = User.objects.create_user(email='user@example.com', password='foo')
        assert user.email == 'user@example.com'
        assert user.is_active
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_superuser(self):
        user = User.objects.create_superuser(email='admin@example.com', password='admin')
        assert user.is_staff
        assert user.is_superuser

    def test_email_normalized(self):
        email = 'Test@Example.COM'
        user = User.objects.create_user(email=email, password='x')
        assert user.email == 'test@example.com'

    def test_email_required(self):
        with pytest.raises(ValueError):
            User.objects.create_user(email='', password='x')

    def test_user_str_is_email(self):
        user = User.objects.create_user(email='user@example.com', password='x')
        assert str(user) == 'user@example.com'


@pytest.mark.django_db
class TestProfileThingRelation:
    def test_profile_belongs_to_thing(self, thing):
        user = User.objects.create_user(email='profile@example.com', password='x')
        profile = Profile.objects.create(user=user, name='Perfil Teste', thing=thing)

        assert profile.thing == thing
        assert profile.thing.thingsgroupid == 'THING-001'

    def test_thing_has_multiple_profiles(self, thing):
        user1 = User.objects.create_user(email='p1@example.com', password='x')
        user2 = User.objects.create_user(email='p2@example.com', password='x')
        Profile.objects.create(user=user1, name='Perfil 1', thing=thing)
        Profile.objects.create(user=user2, name='Perfil 2', thing=thing)

        assert thing.things_profiles.count() == 2


@pytest.mark.django_db
class TestProfileStr:
    def test_str(self, thing):
        user = User.objects.create_user(email='pstr@example.com', password='x')
        profile = Profile.objects.create(user=user, name='Perfil Teste', thing=thing)
        assert str(profile) == 'Profile: Perfil Teste'


@pytest.mark.django_db
class TestProfileSessionsInMonth:
    def test_count_sessions_in_month(self, thing, device):
        user = User.objects.create_user(email='p@example.com', password='x')
        profile = Profile.objects.create(user=user, name='Perfil', thing=thing)

        for i in range(3):
            Session.objects.create(
                device=device, sessionid=f'mar-{i}',
                sessioncreatetime=make_aware(datetime(2026, 3, 15)),
                realusage='100', uom='MB'
            )
        for i in range(2):
            Session.objects.create(
                device=device, sessionid=f'apr-{i}',
                sessioncreatetime=make_aware(datetime(2026, 4, 10)),
                realusage='200', uom='MB'
            )

        count = Session.objects.filter(
            device__thing=profile.thing,
            sessioncreatetime__month=3
        ).count()

        assert count == 3
