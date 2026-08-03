from collections import defaultdict
from datetime import datetime, timedelta

import pandas as pd

MAPEAMENTO_COLUNAS = {
    'sessionid': 'SessionId',
    'sessioncreatetime': 'sessionCreationTime',
    'realusage': 'RealUsage',
}

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
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def _get(row, key, mapping):
    col = mapping.get(key)
    if col and col in row.index:
        val = row[col]
        return None if pd.isna(val) else str(val).strip()
    return None


def analyze_sessions(filepath):
    is_csv = filepath.endswith('.csv')

    if is_csv:
        df = pd.read_csv(filepath, nrows=0)
        columns = list(df.columns)
        mapping = {
            'sessionid': 'SessionId' if 'SessionId' in columns else None,
            'sessioncreatetime': 'sessionCreationTime' if 'sessionCreationTime' in columns else None,
            'realusage': 'RealUsage' if 'RealUsage' in columns else None,
        }
        str_cols = [c for c in columns if c in ('SessionId',)]
        df = pd.read_csv(filepath, dtype={col: str for col in str_cols}, skip_blank_lines=False)
    else:
        mapping = MAPEAMENTO_COLUNAS
        str_cols = ('SessionId',)
        df = pd.read_excel(filepath, dtype={col: str for col in str_cols})

    # Calibracao: mostrar alinhamento de linhas
    total_lidas = len(df)
    if is_csv:
        with open(filepath, 'r', encoding='utf-8') as f:
            total_fisico = sum(1 for _ in f)
    else:
        total_fisico = total_lidas + 1  # aproximacao

    print(f'[CALIBRACAO] Linhas fisicas no arquivo: {total_fisico}')
    print(f'[CALIBRACAO] Linhas lidas pelo pandas:   {total_lidas}')
    if total_lidas > 0:
        print(f'[CALIBRACAO] Primeira linha de dados:     2')
        print(f'[CALIBRACAO] Ultima linha de dados:       {total_lidas + 1}')
    print()

    linhas_por_tripla = defaultdict(list)
    errors = []
    total_vazias = 0

    for idx, linha in df.iterrows():
        # idx = indice do DataFrame (0-based)
        # linha no arquivo = idx + 2 (1-based + header na linha 1)
        linha_no_arquivo = idx + 2
        try:
            session_id = _get(linha, 'sessionid', mapping)
            if not session_id:
                total_vazias += 1
                continue
            raw_dt = linha[mapping['sessioncreatetime']] if mapping.get('sessioncreatetime') and mapping['sessioncreatetime'] in linha.index else None
            sessioncreatetime = _normalize_dt(raw_dt)
            realusage = _get(linha, 'realusage', mapping) or ''
            tripla = (session_id, sessioncreatetime, realusage)
            linhas_por_tripla[tripla].append(linha_no_arquivo)
        except Exception as e:
            errors.append({'line': linha_no_arquivo, 'error': str(e)})

    total_geral = sum(len(v) for v in linhas_por_tripla.values())
    total_repetidas = 0
    total_unicas = 0
    repeated_details = []

    for tripla, linhas in linhas_por_tripla.items():
        count = len(linhas)
        if count > 1:
            total_repetidas += count
            repeated_details.append(tripla + (count, linhas))
        else:
            total_unicas += 1

    print()
    print(f'Arquivo........: {filepath}')
    print(f'Total geral....: {total_geral}')
    print(f'Total vazias...: {total_vazias}')
    print(f'Total repetidas: {total_repetidas}')
    print(f'Total unicas...: {total_unicas}')
    print()

    if repeated_details:
        print('Detalhes das triplas repetidas:')
        for sessionid, sessioncreatetime, realusage, count, linhas in repeated_details:
            linhas_str = ', '.join(str(l) for l in linhas)
            print(f'  - sessionid={sessionid}, sessioncreatetime={sessioncreatetime}, realusage={realusage} -> {count}x (linhas: {linhas_str})')
        print()

    if errors:
        print(f'Erros de parsing ({len(errors)}):')
        for err in errors:
            print(f'  linha {err["line"]}: {err["error"]}')
        print()
