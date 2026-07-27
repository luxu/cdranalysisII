from datetime import datetime, timedelta

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
        return timezone.make_aware(value) if timezone.is_naive(value) else value
    if isinstance(value, str):
        try:
            dt = pd.to_datetime(value)
            return timezone.make_aware(dt) if timezone.is_naive(dt) else dt
        except Exception:
            pass
    return _excel_serial_to_datetime(value)


def _get(row, key, mapping):
    col = mapping.get(key)
    if col and col in row.index:
        val = row[col]
        return None if pd.isna(val) else str(val).strip()
    return None


def _processar_linha(linha, caches, mapping, is_csv):
    org_id = _get(linha, 'orgid', mapping)
    orgname = _get(linha, 'orgname', mapping)

    if is_csv:
        if org_id:
            org_id = org_id.replace("OrganizationId_", "")
        else:
            org_id = orgname or 'UNKNOWN'

    org, _ = Organization.objects.get_or_create(
        orgid=org_id,
        defaults={'orgname': orgname or org_id},
    )
    caches['org'][org_id] = org

    cust_id = _get(linha, 'customerid', mapping)
    customer = None
    if cust_id:
        cust_id = cust_id.replace("cid_", "")
        if cust_id not in caches['customer']:
            customername = _get(linha, 'customername', mapping)
            customer, _ = Customer.objects.get_or_create(
                customerid=cust_id,
                defaults={
                    'customername': customername or cust_id,
                    'organization': org,
                },
            )
            caches['customer'][cust_id] = customer
        customer = caches['customer'][cust_id]
    else:
        default_cust_id = f'auto-{org_id}'
        if default_cust_id not in caches['customer']:
            customer, _ = Customer.objects.get_or_create(
                customerid=default_cust_id,
                defaults={
                    'customername': f'Clientes ({orgname or org_id})',
                    'organization': org,
                },
            )
            caches['customer'][default_cust_id] = customer
        customer = caches['customer'][default_cust_id]

    thing_id = _get(linha, 'thingsgroupid', mapping)
    thingsgroupname = _get(linha, 'thingsgroupname', mapping)

    if is_csv and not thing_id:
        thing_id = thingsgroupname or f'thing-{org_id}'

    if thing_id:
        thing_id = thing_id.replace("ThingsGroupId_", "")
    else:
        thing_id = f'thing-{org_id}'

    if thing_id not in caches['thing']:
        thing, _ = Thing.objects.get_or_create(
            thingsgroupid=thing_id,
            defaults={
                'thingsgroupname': thingsgroupname or thing_id,
                'customer': customer,
            },
        )
        caches['thing'][thing_id] = thing
    thing = caches['thing'][thing_id]

    imsi = _get(linha, 'imsi', mapping)
    if not imsi:
        return

    if imsi not in caches['device']:
        imei = _get(linha, 'imei', mapping) or ''
        device, _ = Device.objects.get_or_create(
            imsi=imsi,
            defaults={
                'imei': imei,
                'thing': thing,
            },
        )
        caches['device'][imsi] = device
    device = caches['device'][imsi]

    session_id = _get(linha, 'sessionid', mapping)
    if not session_id:
        return

    if session_id not in caches['session']:
        raw_dt = linha[mapping['sessioncreatetime']] if mapping['sessioncreatetime'] in linha.index else None
        sessioncreatetime = _parse_datetime(raw_dt)
        realusage = _get(linha, 'realusage', mapping)
        uom = _get(linha, 'uom', mapping)
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

    networkproviderid = _get(linha, 'networkproviderid', mapping)
    if networkproviderid:
        networkproviderid = networkproviderid.replace("NetworkProviderId_", "")
        if networkproviderid not in caches['networkprovider']:
            networkprovidername = _get(linha, 'networkprovidername', mapping)
            NetworkProvider.objects.get_or_create(
                networkproviderid=networkproviderid,
                defaults={
                    'networkprovidername': networkprovidername or networkproviderid,
                    'customer': customer,
                },
            )
            caches['networkprovider'][networkproviderid] = True

    priceplanid = _get(linha, 'priceplanid', mapping)
    if priceplanid:
        priceplanid = priceplanid.replace("PricePlanId_", "")
        if priceplanid not in caches['priceplan']:
            priceplanname = _get(linha, 'priceplanname', mapping)
            PricePlan.objects.get_or_create(
                priceplanid=priceplanid,
                defaults={
                    'priceplanname': priceplanname or priceplanid,
                    'customer': customer,
                },
            )
            caches['priceplan'][priceplanid] = True

    mnoid = _get(linha, 'mnoid', mapping)
    if mnoid:
        mnoid = mnoid.replace("MNOId_", "")
        if mnoid not in caches['mno']:
            mnoname = _get(linha, 'mnoname', mapping)
            Mno.objects.get_or_create(
                mnoid=mnoid,
                defaults={
                    'mnoname': mnoname or mnoid,
                    'organization': org,
                },
            )
            caches['mno'][mnoid] = True


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


def import_cdr_from_file(filepath):
    caches = {
        'org': {}, 'customer': {}, 'thing': {},
        'device': {}, 'session': {}, 'networkprovider': {},
        'priceplan': {}, 'mno': {},
    }

    is_csv = filepath.endswith('.csv')

    if is_csv:
        df = pd.read_csv(filepath, nrows=0)
        columns = list(df.columns)
        mapping = _detect_mapping(columns, is_csv)
        str_cols = [c for c in columns if c in COLUNAS_COMO_STR]
        df = pd.read_csv(filepath, dtype={col: str for col in str_cols})
    else:
        mapping = MAPEAMENTO_COLUNAS
        df = pd.read_excel(filepath, dtype={col: str for col in COLUNAS_COMO_STR})

    total = len(df)
    errors = []

    for i, (_, linha) in enumerate(df.iterrows(), 1):
        try:
            _processar_linha(linha, caches, mapping, is_csv)
        except Exception as e:
            errors.append({'line': i, 'error': str(e)})

    return {
        'total_lines': total,
        'organizations': len(caches['org']),
        'customers': len(caches['customer']),
        'things': len(caches['thing']),
        'devices': len(caches['device']),
        'sessions': len(caches['session']),
        'networkproviders': len(caches['networkprovider']),
        'priceplans': len(caches['priceplan']),
        'mnos': len(caches['mno']),
        'errors': errors[:100],
    }
