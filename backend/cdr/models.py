import uuid

from django.db import models
from core.models import Base


class Organization(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orgid = models.CharField(
        max_length=255,
        unique=True,
    )
    orgname = models.CharField(max_length=255)

    def __str__(self):
        return f'Organization..: {self.orgname}'

class Customer(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customerid = models.CharField(
        max_length=255,
        unique=True,
    )
    customername = models.CharField(max_length=255)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='organization_customers',
    )

    def __str__(self):
        return f'Customer..: {self.customername}'

class Mno(Base):
    # Operadora de rede móvel (ex: Vivo, Claro, Tim).
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    mnoid = models.CharField(
        max_length=255,
        unique=True,
    )
    mnoname = models.CharField(max_length=255)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='mno_organizations',
    )

    class Meta:
        verbose_name = 'Mno(Mobile Network Operator)'
        verbose_name_plural = 'Mnos(Mobile Network Operator)'

    def __str__(self):
        return f'MNO..: {self.mnoid}'


class NetworkProvider(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    networkproviderid = models.CharField(
        max_length=255,
        unique=True,
    )
    networkprovidername = models.CharField(max_length=255)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='networkprovider_customers',
    )

    def __str__(self):
        return f'NetworkProvider..: {self.networkprovidername}'


class PricePlan(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    priceplanid = models.CharField(
        max_length=255,
        unique=True,
    )
    priceplanname = models.CharField(max_length=255)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='priceplan_customers',
    )

    def __str__(self):
        return f'PricePlan..: {self.priceplanname}'


class Thing(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thingsgroupid = models.CharField(
        max_length=255,
        unique=True,
    )
    thingsgroupname = models.CharField(max_length=255)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='things_customers',
    )

    def __str__(self):
        return f'Thing..: {self.thingsgroupname}'

    class Meta:
        verbose_name = 'Dispositivo(Thing)'
        verbose_name_plural = 'Dispositivos(Things)'
