import uuid
from django.db import models

from core.models import Base


class Device(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # iccid = models.CharField(
    #     'ICCID(ID do cartão SIM)',
    #     max_length=255,
    # )  # ThingName só os nros
    imsi = models.CharField(
        "IMSI(Internacional Mobile Subscriber Identity)",
        max_length=255,
    )  # (FK)
    # msisdn = models.CharField(
    #     "MSISDN(número da linha)",
    #     max_length=255,
    # )
    # mei = models.CharField(
    #     "MEI(ID do aparelho)",
    #     max_length=255,
    # )
    # status = models.CharField(
    #     max_length=255,
    # )


class Session(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    imsi = models.CharField(
        "IMSI(Internacional Mobile Subscriber Identity)",
        max_length=255,
    )  # (FK)
    realusage = models.CharField(
        "RealUsage1(consumo real)",
        max_length=255,
    )
    uom = models.CharField(
        "UOM(Unidade de Medida, ex: MB, KB)",
        max_length=255,
    )
