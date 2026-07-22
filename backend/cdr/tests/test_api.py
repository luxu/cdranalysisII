import pytest
from datetime import datetime

from django.urls import reverse
from django.utils.timezone import make_aware

from cdr.models import Session


pytestmark = pytest.mark.django_db


class TestDeviceFilterAPI:
    def test_filter_by_thing(self, authenticated_client, thing, device):
        url = reverse('device-list')
        resp = authenticated_client.get(url, {'thing': thing.id})
        assert resp.status_code == 200
        assert len(resp.data['results']) == 1

    def test_filter_by_search_imsi(self, authenticated_client, thing, device):
        url = reverse('device-list')
        resp = authenticated_client.get(url, {'search': 'IMSI'})
        assert resp.status_code == 200
        assert len(resp.data['results']) == 1

    def test_filter_by_search_msisdn(self, authenticated_client, thing, device):
        url = reverse('device-list')
        resp = authenticated_client.get(url, {'search': '999999'})
        assert resp.status_code == 200
        assert len(resp.data['results']) == 1

    def test_filter_by_status_active(self, authenticated_client, thing, device):
        url = reverse('device-list')
        resp = authenticated_client.get(url, {'status': 'true'})
        assert resp.status_code == 200
        assert len(resp.data['results']) == 1

    def test_filter_by_thing_no_match(self, authenticated_client, thing):
        url = reverse('device-list')
        resp = authenticated_client.get(url, {'thing': '00000000-0000-0000-0000-000000000000'})
        assert resp.status_code == 200
        assert len(resp.data['results']) == 0

    def test_filter_requires_auth(self, client, thing, device):
        url = reverse('device-list')
        resp = client.get(url, {'thing': thing.id})
        assert resp.status_code == 403


class TestSessionFilterAPI:
    def test_filter_by_device_thing(self, authenticated_client, user, thing, device):
        Session.objects.create(
            device=device, sessionid='SESS-FILTER',
            sessioncreatetime=make_aware(datetime(2026, 1, 1)),
            realusage='100', uom='MB',
        )
        url = reverse('session-list')
        resp = authenticated_client.get(url, {'device__thing': thing.id})
        assert resp.status_code == 200
        assert len(resp.data['results']) == 1

    def test_filter_by_device_thing_no_match(self, authenticated_client, thing):
        url = reverse('session-list')
        resp = authenticated_client.get(url, {'device__thing': '00000000-0000-0000-0000-000000000000'})
        assert resp.status_code == 200
        assert len(resp.data['results']) == 0

    def test_filter_requires_auth(self, client, thing):
        url = reverse('session-list')
        resp = client.get(url, {'device__thing': thing.id})
        assert resp.status_code == 403
