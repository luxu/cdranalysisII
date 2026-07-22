import pytest
from datetime import datetime

from django.urls import reverse
from django.utils.timezone import make_aware

from django.contrib.auth import get_user_model

from cdr.models import Organization, Customer, Thing, Device, Session
from user.models import Profile

User = get_user_model()


pytestmark = pytest.mark.django_db


class TestProfileSessionCountAPI:
    def test_session_count_in_month(self, authenticated_client, user, thing, device):
        profile = Profile.objects.create(user=user, name='Perfil', thing=thing)

        for i in range(3):
            Session.objects.create(
                device=device, sessionid=f'mar-{i}',
                sessioncreatetime=make_aware(datetime(2026, 3, 15)),
                realusage='100', uom='MB',
            )
        for i in range(2):
            Session.objects.create(
                device=device, sessionid=f'apr-{i}',
                sessioncreatetime=make_aware(datetime(2026, 4, 10)),
                realusage='200', uom='MB',
            )

        url = reverse('profile-session-count', kwargs={'pk': profile.id})
        resp = authenticated_client.get(url, {'month': 3})

        assert resp.status_code == 200
        assert resp.data['session_count'] == 3
        assert resp.data['month'] == 3

    def test_session_count_zero_when_none(self, authenticated_client, user, thing, device):
        profile = Profile.objects.create(user=user, name='Perfil', thing=thing)

        url = reverse('profile-session-count', kwargs={'pk': profile.id})
        resp = authenticated_client.get(url, {'month': 6})

        assert resp.status_code == 200
        assert resp.data['session_count'] == 0

    def test_session_count_requires_month_param(self, authenticated_client, user, thing, device):
        profile = Profile.objects.create(user=user, name='Perfil', thing=thing)

        url = reverse('profile-session-count', kwargs={'pk': profile.id})
        resp = authenticated_client.get(url)

        assert resp.status_code == 400
        assert 'month' in resp.data['error']

    def test_session_count_requires_auth(self, client, thing, device, user):
        profile = Profile.objects.create(user=user, name='Perfil', thing=thing)

        url = reverse('profile-session-count', kwargs={'pk': profile.id})
        resp = client.get(url, {'month': 3})

        assert resp.status_code == 403


class TestLoginAPI:
    def test_login_success(self, client):
        User.objects.create_user(email='login@example.com', password='secret123')
        resp = client.post('/api/auth/login/', {
            'email': 'login@example.com', 'password': 'secret123',
        })
        assert resp.status_code == 200
        assert 'token' in resp.data

    def test_login_invalid_credentials(self, client):
        resp = client.post('/api/auth/login/', {
            'email': 'noone@example.com', 'password': 'wrong',
        })
        assert resp.status_code == 400

    def test_login_inactive_user(self, client):
        user = User.objects.create_user(
            email='inactive@example.com', password='secret123',
        )
        user.is_active = False
        user.save()
        resp = client.post('/api/auth/login/', {
            'email': 'inactive@example.com', 'password': 'secret123',
        })
        assert resp.status_code == 400


class TestProfileSessionsAPI:
    def test_sessions_returns_only_profile_sessions(self, authenticated_client, user, thing, device):
        profile = Profile.objects.create(user=user, name='Perfil', thing=thing)

        for i in range(3):
            Session.objects.create(
                device=device, sessionid=f'mine-{i}',
                sessioncreatetime=make_aware(datetime(2026, 1, 1)),
                realusage='100', uom='MB',
            )

        url = reverse('profile-sessions', kwargs={'pk': profile.id})
        resp = authenticated_client.get(url)

        assert resp.status_code == 200
        assert len(resp.data) == 3
        assert {s['sessionid'] for s in resp.data} == {'mine-0', 'mine-1', 'mine-2'}

    def test_sessions_excludes_other_profiles(self, authenticated_client, user, thing, device):
        profile = Profile.objects.create(user=user, name='Perfil', thing=thing)
        Session.objects.create(
            device=device, sessionid='own',
            sessioncreatetime=make_aware(datetime(2026, 1, 1)),
            realusage='100', uom='MB',
        )

        other_org = Organization.objects.create(orgid='ORG-O', orgname='Outra')
        other_cust = Customer.objects.create(
            customerid='CUST-O', customername='Outro', organization=other_org,
        )
        other_thing = Thing.objects.create(
            thingsgroupid='THING-O', thingsgroupname='Outro', customer=other_cust,
        )
        other_device = Device.objects.create(
            thing=other_thing, imsi='OTHER', msisdn='0', imei='0',
        )
        Session.objects.create(
            device=other_device, sessionid='other',
            sessioncreatetime=make_aware(datetime(2026, 1, 1)),
            realusage='200', uom='MB',
        )

        url = reverse('profile-sessions', kwargs={'pk': profile.id})
        resp = authenticated_client.get(url)

        assert resp.status_code == 200
        assert len(resp.data) == 1
        assert resp.data[0]['sessionid'] == 'own'

    def test_sessions_requires_auth(self, client, thing, device, user):
        profile = Profile.objects.create(user=user, name='Perfil', thing=thing)

        url = reverse('profile-sessions', kwargs={'pk': profile.id})
        resp = client.get(url)

        assert resp.status_code == 403
