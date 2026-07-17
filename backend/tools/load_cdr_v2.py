import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kernel.settings')

import django
django.setup()

import pandas as pd
from django.utils import timezone

from cdr.models import (
    Organization,
    Customer,
    Thing,
    Device,
    Session,
)

MAPEAMENTO_COLUNAS = {
    'orgid': 'OrganizationId',
    'orgname': 'OrganizationName',
    'customerid': 'CustomerId',
    'customername': 'CustomerName',
    'thingsgroupid': 'ThingsGroupId',
    'thingsgroupname': 'ThingsGroupName',
    'imsi': 'IMSI',
    'msisdn': 'MSISDN',
    'sessionid': 'SessionId',
    'sessioncreatetime': 'sessionCreationTime',
}

COLUNAS_COMO_STR = [
    'OrganizationId', 'CustomerId', 'ThingsGroupId',
    'IMSI', 'MSISDN', 'SessionId',
]


def load_file(filename):
    return pd.read_excel(filename, dtype={col: str for col in COLUNAS_COMO_STR})


def processar_linha(linha, caches):
    m = MAPEAMENTO_COLUNAS

    org_id = linha[m['orgid']]
    org, _ = Organization.objects.get_or_create(
        orgid=org_id,
        defaults={'orgname': linha[m['orgname']]},
    )
    caches['org'][org_id] = org

    cust_id = linha[m['customerid']]
    if cust_id not in caches['customer']:
        customer, _ = Customer.objects.get_or_create(
            customerid=cust_id,
            defaults={
                'customername': linha[m['customername']],
                'organization': org,
            },
        )
        caches['customer'][cust_id] = customer
    customer = caches['customer'][cust_id]

    thing_id = linha[m['thingsgroupid']]
    if thing_id not in caches['thing']:
        thing, _ = Thing.objects.get_or_create(
            thingsgroupid=thing_id,
            defaults={
                'thingsgroupname': linha[m['thingsgroupname']],
                'customer': customer,
            },
        )
        caches['thing'][thing_id] = thing
    thing = caches['thing'][thing_id]

    imsi = linha[m['imsi']]
    if imsi not in caches['device']:
        device, _ = Device.objects.get_or_create(
            imsi=imsi,
            defaults={
                'msisdn': linha[m['msisdn']],
                'thing': thing,
            },
        )
        caches['device'][imsi] = device
    device = caches['device'][imsi]

    session_id = linha[m['sessionid']]
    if pd.isna(session_id):
        return

    if session_id not in caches['session']:
        sessioncreatetime_ = linha[m['sessioncreatetime']]
        if pd.isna(sessioncreatetime_):
            sessioncreatetime_ = None
        else:
            sessioncreatetime_ = timezone.make_aware(sessioncreatetime_)

        Session.objects.get_or_create(
            sessionid=session_id,
            defaults={
                'sessioncreatetime': sessioncreatetime_,
                'imsi': imsi,
                'device': device,
            },
        )
        caches['session'][session_id] = True


if __name__ == '__main__':
    filename = os.path.join(os.path.dirname(__file__), '..', 'files', 'cdr.xlsx')
    df = load_file(filename)

    caches = {
        'org': {},
        'customer': {},
        'thing': {},
        'device': {},
        'session': {},
    }

    total = len(df)
    print(f"Iniciando carga de {total} registros...")

    for i, (_, linha) in enumerate(df.iterrows(), 1):
        processar_linha(linha, caches)
        if i % 100 == 0 or i == total:
            print(f"  Processadas {i}/{total} linhas...")

    print("\nCarga finalizada com sucesso!")
    print(f"  Organizations: {len(caches['org'])}")
    print(f"  Customers:     {len(caches['customer'])}")
    print(f"  Things:        {len(caches['thing'])}")
    print(f"  Devices:       {len(caches['device'])}")
    print(f"  Sessions:      {len(caches['session'])}")
