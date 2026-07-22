import pytest
from datetime import datetime

from django.utils.timezone import make_aware

from cdr.models import Mno, NetworkProvider, PricePlan, Session


pytestmark = pytest.mark.django_db


class TestOrganizationStr:
    def test_str(self, organization):
        assert str(organization) == 'Organization..: Org Teste'


class TestCustomerStr:
    def test_str(self, customer):
        assert str(customer) == 'Customer..: Cliente Teste'


class TestMnoStr:
    def test_str(self, organization):
        mno = Mno.objects.create(mnoid='MNO-001', mnoname='Vivo', organization=organization)
        assert str(mno) == 'Vivo'


class TestNetworkProviderStr:
    def test_str(self, customer):
        np = NetworkProvider.objects.create(
            networkproviderid='NP-001', networkprovidername='Provedor X',
            customer=customer,
        )
        assert str(np) == 'NetworkProvider..: Provedor X'


class TestPricePlanStr:
    def test_str(self, customer):
        pp = PricePlan.objects.create(
            priceplanid='PP-001', priceplanname='Plano Premium', customer=customer,
        )
        assert str(pp) == 'PricePlan..: Plano Premium'


class TestThingStr:
    def test_str(self, thing):
        assert str(thing) == 'Grupo Teste'


class TestDeviceStr:
    def test_str(self, device):
        assert str(device) == 'IMSI-001'


class TestSessionStr:
    def test_str(self, device):
        session = Session.objects.create(
            device=device, sessionid='SESS-001',
            sessioncreatetime=make_aware(datetime(2026, 1, 1)),
            realusage='100', uom='MB',
        )
        assert str(session) == 'SESS-001'
