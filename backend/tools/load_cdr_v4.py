import os
import sys
from datetime import datetime, timedelta

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
    NetworkProvider,
    PricePlan,
    Mno,
)

MAPEAMENTO_COLUNAS = {
    'orgid': 'OrganizationId',
    'orgname': 'OrganizationName',
    'customerid': 'CustomerId',
    'customername': 'CustomerName',
    'thingsgroupid': 'ThingsGroupId',
    'thingsgroupname': 'ThingsGroupName',
    'imsi': 'IMSI',
    'imei': 'IMEI',
    'sessionid': 'SessionId',
    'sessioncreatetime': 'sessionCreationTime',
    'realusage': 'RealUsage',
    'uom': 'UOM',
    'networkproviderid': 'NetworkProviderId',
    'networkprovidername': 'NetworkProviderName',
    'priceplanid': 'PricePlanId',
    'priceplanname': 'PricePlanName',
    'mnoid': 'MNOId',
    'mnoname': 'MnoName',
}

COLUNAS_COMO_STR = [
    'OrganizationId', 'CustomerId', 'ThingsGroupId',
    'IMSI', 'SessionId', 'NetworkProviderId',
    'PricePlanId', 'MNOId'
]

EXCEL_EPOCH = datetime(1899, 12, 30)


def _excel_serial_to_datetime(serial):
    try:
        val = float(serial)
    except (ValueError, TypeError):
        return None
    if val < 1:
        return None
    return EXCEL_EPOCH + timedelta(days=val)


def _parse_datetime(value):
    if pd.isna(value):
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return pd.to_datetime(value).to_pydatetime()
        except Exception:
            pass
    return _excel_serial_to_datetime(value)


def _normalize_dt(value):
    dt = _parse_datetime(value)
    if dt is None:
        return None
    if dt.tzinfo is not None:
        dt = dt.replace(tzinfo=None)
    return timezone.make_aware(dt)


"""
Linhas 199–204 inicializam o dicionário `caches` com chaves `org`,
`customer`, `thing`, `device`, `session` — cada uma mapeando para um dict vazio.
Serve como cache em memória para evitar consultas repetidas ao banco:
quando `processar_linha` processa uma linha, ela primeiro verifica se a entidade
já está no cache; se sim, reusa o objeto em vez de buscar/criar no banco de novo.
"""
CACHES = {
    'org': {},
    'customer': {},
    'thing': {},
    'device': {},
    'networkprovider': {},
    'priceplan': {},
    'mno': {},
}

SESSION_STATS = {'saved': 0, 'empty': 0, 'duplicate': 0}
SESSION_BATCH_SIZE = 1000


def load_file(filename):
    return pd.read_csv(filename, dtype={col: str for col in COLUNAS_COMO_STR})
    # return pd.read_excel(filename, dtype={col: str for col in COLUNAS_COMO_STR})

def _detect_mapping(columns, is_csv):
    if is_csv:
        return {
            'orgid': 'OrganizationId' if 'OrganizationId' in columns else None,
            'orgname': 'OrganizationName' if 'OrganizationName' in columns else None,
            'customerid': 'CustomerId' if 'CustomerId' in columns else None,
            'customername': 'CustomerName' if 'CustomerName' in columns else None,
            'thingsgroupid': 'ThingsGroupId' if 'ThingsGroupId' in columns else None,
            'thingsgroupname': 'ThingsGroupName' if 'ThingsGroupName' in columns else None,
            'imsi': 'IMSI',
            'imei': 'IMEI',
            'sessionid': 'SessionId',
            'sessioncreatetime': 'sessionCreationTime',
            'realusage': 'RealUsage' if 'RealUsage' in columns else None,
            'uom': 'UOM' if 'UOM' in columns else None,
            'networkproviderid': 'NetworkProviderId' if 'NetworkProviderId' in columns else None,
            'networkprovidername': 'NetworkProviderName' if 'NetworkProviderName' in columns else None,
            'priceplanid': 'PricePlanId' if 'PricePlanId' in columns else None,
            'priceplanname': 'PricePlanName' if 'PricePlanName' in columns else None,
            'mnoid': 'MNOId' if 'MNOId' in columns else None,
            'mnoname': 'MnoName' if 'MnoName' in columns else None,
        }
    return MAPEAMENTO_COLUNAS

def _processar_linha(linha, caches, mapping, is_csv, sessions_batch):
    """
    A linha 80 usa `get_or_create` do Django ORM:
    busca um `Organization` com `orgid=org_id` no banco; 
    se não existir, cria um novo com `orgname` extraído da planilha. 
    O `_` descarta o booleano que indica se foi criado ou não.
    """
    # ******************************************************************** ORGANIZATION *****************
    org_id = linha[MAPEAMENTO_COLUNAS['orgid']]
    org_id = org_id.replace("OrganizationId_", "")
    orgname = linha[MAPEAMENTO_COLUNAS['orgname']]

    org, _ = Organization.objects.get_or_create(
        orgid=org_id,  # Pesquisa no banco se existe dados iguais
        defaults={
            'orgname': orgname
        },
    )
    caches['org'][org_id] = org
    # ******************************************************************** CUSTOMER *****************
    cust_id = linha[MAPEAMENTO_COLUNAS['customerid']]
    cust_id = cust_id.replace("cid_", "")
    # cid_4363b0be-4d72-49fd-995b-51a5ba2598e1
    if cust_id not in caches['customer']:
        customername = linha[MAPEAMENTO_COLUNAS['customername']]
        customer, _ = Customer.objects.get_or_create(
            customerid=cust_id,
            defaults={
                'customername': customername,
                'organization': org,
            },
        )
        caches['customer'][cust_id] = customer
    customer = caches['customer'][cust_id]
    # ******************************************************************** THING *****************
    thing_id = linha[MAPEAMENTO_COLUNAS['thingsgroupid']]
    if thing_id not in caches['thing']:
        thing_id = thing_id.replace("ThingsGroupId_", "")
        thingsgroupname = linha[MAPEAMENTO_COLUNAS['thingsgroupname']]
        thing, _ = Thing.objects.get_or_create(
            thingsgroupid=thing_id,
            defaults={
                'thingsgroupname': thingsgroupname,
                'customer': customer,
            },
        )
        caches['thing'][thing_id] = thing
    thing = caches['thing'][thing_id]
    # ******************************************************************** DEVICE *****************
    imsi = linha[MAPEAMENTO_COLUNAS['imsi']]
    iccid = linha[MAPEAMENTO_COLUNAS['imsi']].replace("ThingId_ICCID_", "")
    if imsi not in caches['device']:
        imei = linha[MAPEAMENTO_COLUNAS['imei']]
        device, _ = Device.objects.get_or_create(
            imsi=imsi,
            defaults={
                'iccid': iccid,
                'imei': imei,
                'thing': thing,
            },
        )
        caches['device'][imsi] = device
    device = caches['device'][imsi]

    # ******************************************************************** NETWORK PROVIDERS *****************
    networkproviderid = linha[MAPEAMENTO_COLUNAS['networkproviderid']]
    networkproviderid = networkproviderid.replace("NetworkProviderId_", "")
    if networkproviderid not in caches['networkprovider']:
        networkprovidername = linha[MAPEAMENTO_COLUNAS['networkprovidername']]
        NetworkProvider.objects.get_or_create(
            networkproviderid=networkproviderid,
            defaults={
                'networkprovidername': networkprovidername,
                'customer': customer,
            }
        )
        caches['networkprovider'][networkproviderid] = True

    # ******************************************************************** MNOS *****************
    mnoid = linha[MAPEAMENTO_COLUNAS['mnoid']]
    mnoid = mnoid.replace("MNOId_", "")
    if mnoid not in caches['mno']:
        mnoname = linha[MAPEAMENTO_COLUNAS['mnoname']]
        Mno.objects.get_or_create(
            mnoid=mnoid,
            defaults={
                'mnoname': mnoname,
                'organization': org,
            }
        )
        caches['mno'][mnoid] = True

    # ******************************************************************** SESSION *****************
    session_id = linha[MAPEAMENTO_COLUNAS['sessionid']]
    session_id = '' if pd.isna(session_id) else str(session_id).strip()

    raw_dt = linha[MAPEAMENTO_COLUNAS['sessioncreatetime']]
    sessioncreatetime_norm = _normalize_dt(raw_dt) or timezone.now()

    realusage = linha[MAPEAMENTO_COLUNAS['realusage']]
    realusage = '' if pd.isna(realusage) else str(realusage).strip()
    uom = '' if pd.isna(linha[MAPEAMENTO_COLUNAS['uom']]) else str(linha[MAPEAMENTO_COLUNAS['uom']]).strip()

    session = Session(
        sessionid=session_id,
        sessioncreatetime=sessioncreatetime_norm,
        device=device,
        realusage=realusage,
        uom=uom,
    )
    sessions_batch.append(session)

    # ******************************************************************** PRICE PLANS *****************
    priceplanid = linha[MAPEAMENTO_COLUNAS['priceplanid']]
    priceplanid = priceplanid.replace("PricePlanId_", "")
    if pd.isna(priceplanid):
        return

    if priceplanid not in caches['priceplan']:
        priceplanname = linha[MAPEAMENTO_COLUNAS['priceplanname']]
        PricePlan.objects.get_or_create(
            priceplanid=priceplanid,
            defaults={
                'priceplanname': priceplanname,
                'customer': customer,
            }
        )
        caches['priceplan'][priceplanid] = True

if __name__ == '__main__':
    files_dir = os.path.join(os.path.dirname(__file__), '..', 'files')
    # files_dir = r'C:\Users\luxu\Desktop\cdr'
    filenames = [
        os.path.join(files_dir, f)
        for f in os.listdir(files_dir)
        if f.lower().endswith(('.csv', '.xlsx', '.xls'))
    ]

    for filename in filenames:
        print(f"\nProcessando arquivo: {os.path.basename(filename)}")

        is_csv = filename.lower().endswith('.csv')

        if is_csv:
            df = pd.read_csv(filename, nrows=0)
            columns = list(df.columns)
            mapping = _detect_mapping(columns, is_csv)
            str_cols = [c for c in columns if c in COLUNAS_COMO_STR]
            df = pd.read_csv(filename, dtype={col: str for col in str_cols})
        else:
            mapping = MAPEAMENTO_COLUNAS
            df = pd.read_excel(filename, dtype={col: str for col in COLUNAS_COMO_STR})

        total = len(df)
        errors = []
        sessions_batch = []
        print(f"Iniciando carga de {total} registros...")

        """
        `df.iterrows()` retorna pares `(índice_do_dataframe, série_com_a_linha)`.
        O `_` descarta o índice original do pandas (não usado), `linha` recebe os dados da linha.
        Resumindo: itera as linhas da planilha com um número sequencial para o log,
        ignorando o índice numérico que o pandas já tem.
        """
        for i, (_, linha) in enumerate(df.iterrows(), 1):
            try:
                _processar_linha(linha, CACHES, mapping, is_csv, sessions_batch)
            except Exception as e:
                errors.append({'file': os.path.basename(filename), 'line': i, 'error': str(e)})
            if len(sessions_batch) >= SESSION_BATCH_SIZE:
                Session.objects.bulk_create(sessions_batch)
                SESSION_STATS['saved'] += len(sessions_batch)
                sessions_batch.clear()
            if i % 100 == 0 or i == total:
                print(f"  Processadas {i}/{total} linhas...")

        if sessions_batch:
            Session.objects.bulk_create(sessions_batch)
            SESSION_STATS['saved'] += len(sessions_batch)
            sessions_batch.clear()

    print("\nCarga finalizada com sucesso!")
    print(f"  Organizations:   {len(CACHES['org'])}")
    print(f"  Customers:       {len(CACHES['customer'])}")
    print(f"  Mno:             {len(CACHES['mno'])}")
    print(f"  Networkprovider: {len(CACHES['networkprovider'])}")
    print(f"  Priceplan:       {len(CACHES['priceplan'])}")
    print(f"  Things:          {len(CACHES['thing'])}")
    print(f"  Devices:         {len(CACHES['device'])}")
    print(f"  Sessions:        {SESSION_STATS['saved']}")
    print()
    print("  Session Stats:")
    print(f"    Saved:     {SESSION_STATS['saved']}")
    print(f"    Empty:     {SESSION_STATS['empty']}")
    print(f"    Duplicate: {SESSION_STATS['duplicate']}")
    print(f'errors: {errors[:100]}')