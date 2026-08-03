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
    'session': {},
    'networkprovider': {},
    'priceplan': {},
    'mno': {},
}


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

def _processar_linha(linha, caches, mapping, is_csv):
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
    if imsi not in caches['device']:
        imei = linha[MAPEAMENTO_COLUNAS['imei']]
        device, _ = Device.objects.get_or_create(
            imsi=imsi,
            defaults={
                'imei': imei,
                'thing': thing,
            },
        )
        caches['device'][imsi] = device
    device = caches['device'][imsi]
    # ******************************************************************** SESSION *****************
    session_id = linha[MAPEAMENTO_COLUNAS['sessionid']]
    # Se a célula Session estiver em branco retorna
    if pd.isna(session_id):
        return

    if session_id not in caches['session']:
        sessioncreatetime = linha[MAPEAMENTO_COLUNAS['sessioncreatetime']]
        sessioncreatetime = None if pd.isna(sessioncreatetime) else timezone.make_aware(sessioncreatetime)
        realusage = linha[MAPEAMENTO_COLUNAS['realusage']] if not pd.isna(
            linha[MAPEAMENTO_COLUNAS['realusage']]) else None
        uom = linha[MAPEAMENTO_COLUNAS['uom']] if not pd.isna(linha[MAPEAMENTO_COLUNAS['uom']]) else None
        Session.objects.get_or_create(
            sessionid=session_id,
            defaults={
                'sessioncreatetime': sessioncreatetime,
                'device': device,
                'realusage': realusage,
                'uom': uom,
            },
        )
        caches['session'][session_id] = True
    # ******************************************************************** NETWORK PROVIDERS *****************
    networkproviderid = linha[MAPEAMENTO_COLUNAS['networkproviderid']]
    networkproviderid = networkproviderid.replace("NetworkProviderId_", "")
    # NetworkProviderId_57afa6a5-a642-4d01-92f8-87880964264c
    # Se a célula Network Provider estiver em branco retorna
    if pd.isna(session_id):
        return

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

    # ******************************************************************** PRICE PLANS *****************
    priceplanid = linha[MAPEAMENTO_COLUNAS['priceplanid']]
    priceplanid = priceplanid.replace("PricePlanId_", "")
    # PricePlanId_0e61e5d4-300a-4be6-8d9a-868c185f7044
    # Se a célula Price Plan estiver em branco retorna
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

    # ******************************************************************** MNOS *****************
    mnoid = linha[MAPEAMENTO_COLUNAS['mnoid']]
    mnoid = mnoid.replace("MNOId_", "")
    # MNOId_48d1f9c1-283a-45ea-8f09-50a75f8f80b9
    # Se a célula Mno estiver em branco retorna
    if pd.isna(session_id):
        return

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


if __name__ == '__main__':
    filename = os.path.join(os.path.dirname(__file__), '..', 'files', 'cdr.csv')

    is_csv = filename.endswith('.csv')

    df = load_file(filename)

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
    print(f"Iniciando carga de {total} registros...")

    """
    `df.iterrows()` retorna pares `(índice_do_dataframe, série_com_a_linha)`. 
    O `_` descarta o índice original do pandas (não usado), `linha` recebe os dados da linha. 
    Resumindo: itera as linhas da planilha com um número sequencial para o log, 
    ignorando o índice numérico que o pandas já tem.
    """
    for i, (_, linha) in enumerate(df.iterrows(), 1):
        try:
            _processar_linha(linha, CACHES, mapping, is_csv)
        except Exception as e:
            errors.append({'line': i, 'error': str(e)})
        if i % 100 == 0 or i == total:
            print(f"  Processadas {i}/{total} linhas...")

    print("\nCarga finalizada com sucesso!")
    print(f"  Organizations:   {len(CACHES['org'])}")
    print(f"  Customers:       {len(CACHES['customer'])}")
    print(f"  Mno:             {len(CACHES['mno'])}")
    print(f"  Networkprovider: {len(CACHES['networkprovider'])}")
    print(f"  Priceplan:       {len(CACHES['priceplan'])}")
    print(f"  Things:          {len(CACHES['thing'])}")
    print(f"  Devices:         {len(CACHES['device'])}")
    print(f"  Sessions:        {len(CACHES['session'])}")
    print(f'errors: {errors[:100]}')
