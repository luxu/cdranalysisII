import os
import sys
import django
from django.core.exceptions import FieldError

# Adiciona a raiz do projeto (backend/) ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 1. Altere 'nome_do_seu_projeto' para o nome da pasta principal do seu projeto Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','kernel.settings')

# 2. Inicializa o Django
django.setup()

import pandas as pd

from cdr.models import (
    Organization,
    Mno,
    Customer,
    NetworkProvider,
    PricePlan,
    Thing,
    Device,
    Session
)
# Serve para passar o campo dinamicamente na linha 104
MODELS_MAP = {
    'organization': Organization,
    'customer': Customer,
    'mno': Mno,
    'priceplan': PricePlan,
    'networkprovider': NetworkProvider,
    'thing': Thing,
    'device': Device,
    'session': Session,
}
# campo_bd: coluna do excel
MAPEAMENTO_COLUNAS = {
    'orgid': 'OrganizationId',
    'orgname': 'OrganizationName',
    'customerid': 'CustomerId',
    'customername': 'CustomerName',
    'priceplanid': 'PricePlanId',
    'priceplanname': 'PricePlanName',
    'mnoid': 'MNOId',
    'mnoname': 'MnoName',
    'networkproviderid': 'NetworkProviderId',
    'networkprovidername': 'NetworkProviderName',
    'thingsgroupid': 'ThingsGroupId',
    'thingsgroupname': 'ThingsGroupName',
    'imsi': 'imsi'.upper(),
    'msisdn': 'msisdn'.upper(),
    'sessionid': 'SessionId',
    'sessioncreatetime': 'sessionCreationTime'
}


def load_file(filename):
    return pd.read_excel(filename)

def importar_sistema_dinamico(
        df,
        model_django,
        chave_id,
        chave_nome,
        lista_fks=None
):
    mapeamento = MAPEAMENTO_COLUNAS
    coluna_excel_id = mapeamento[chave_id]
    coluna_excel_nome = mapeamento[chave_nome]
    if chave_id == 'sessionid':
        print(chave_id)
        # coluna_excel_id = coluna_excel_id.upper()
        # coluna_excel_nome = coluna_excel_nome.upper()
    colunas_necessarias = [coluna_excel_id, coluna_excel_nome]
    for chave_fk, _ in lista_fks:
        colunas_necessarias.append(mapeamento[chave_fk])
    contador = 0
    # Percorre linha a linha da planilha
    for _, linha in df.iterrows():
        id_excel = linha[coluna_excel_id]
        nome_excel = linha[coluna_excel_nome]
        dados_campos = {
            chave_id: id_excel,
            chave_nome: nome_excel
        }
        objetos_para_criar = []
        if not lista_fks:
            if model_django.objects.filter(orgid=id_excel).exists():
                print(f'Retornando o model..:{model_django.__name__} pois já está cadastrado no BD!')
                return
            objetos_para_criar.append(model_django(**dados_campos))
            model_django.objects.bulk_create(objetos_para_criar)
            print(f'Salvando o model..:{model_django.__name__} pois ele não tem FK!')
            return
        for chave_fk, model_fk in lista_fks:
            coluna_excel_fk = mapeamento[chave_fk]
            id_fk = linha[coluna_excel_fk]
            try:
                if model_django.objects.filter(**{chave_id: id_excel}).exists():
                    print(f'Já está salvo model..:{model_django.__name__} no BD. Continue!')
                    continue
            except FieldError as e:
                print(e)
            try:
                # Pega um FK para salvar no model atual
                model_classe = MODELS_MAP[model_fk]
                instancia_fk = model_classe.objects.get(**{chave_fk: id_fk})
            except Exception:
                print(f'O model..:{model_fk} com {chave_fk}={id_fk} não existe. Reveja!')
                exit()
            dados_campos = {
                chave_id: id_excel,
                chave_nome: nome_excel,
                model_fk: instancia_fk
            }
            try:
                objetos_para_criar.append(model_django(**dados_campos))
                model_django.objects.bulk_create(objetos_para_criar)
                print(f'Perfeito! Model..:{model_django.__name__} salvo no BD!')
            except ValueError as e:
                print(e)
        contador += 1
    print(f'Model:{model_django} \nPassou pelo Arquivo...{contador} vezes!')
    return



if '__main__' == __name__:
    filename = os.path.join(os.path.dirname(__file__), '..', 'files', 'cdr.xlsx')
    df_excel = load_file(filename)
    # uso (Model, primeiro_campo_do_bd, segundo_campo_do_bd, FK(campo, model)
    fila_importacao = [
        (Organization, 'orgid', 'orgname', []),
        (Customer, 'customerid', 'customername', [('orgid', 'organization')]),
        (Thing, 'thingsgroupid', 'thingsgroupname', [('customerid', 'customer')]),
        (Device, 'imsi', 'msisdn', [('thingsgroupid', 'thing')]),
        (Session, 'sessionid', 'sessioncreatetime', [('imsi', 'device')]),
        ### Dependem do ORGANIZATION só
        (Mno, 'mnoid', 'mnoname', [('orgid', 'organization')]),
        (PricePlan, 'priceplanid', 'priceplanname', [('customerid', 'customer')]),
        (NetworkProvider, 'networkproviderid', 'networkprovidername', [('customerid', 'customer')]),
    ]
    print("Iniciando carga de dados integrada...")
    for model, campo_id, campo_nome, fks in fila_importacao:
        print(f"\nProcessando model: {model.__name__}...")
        importar_sistema_dinamico(
            df=df_excel,
            model_django=model,
            chave_id=campo_id,
            chave_nome=campo_nome,
            lista_fks=fks
        )
    print("\nCarga finalizada com sucesso!")
