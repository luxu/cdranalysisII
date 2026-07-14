import csv
import os

from tabulate import tabulate


class Csv:
    def __init__(self, filename):
        self.filename = filename
        self.dados = []
        self.number_lines = 0
        self.number_columns = 0
        self.cabecalhos = None
        self.ws = self.load_csv()

    def get_number_columns(self):
        self.number_columns = len(self.cabecalhos)

    def get_name_columns(self):
        self.load_cabecalhos()
        for name in self.cabecalhos:
            print(name)
        print(self.cabecalhos)

    def load_csv(self):
        self.load_cabecalhos()
        self.read_filename()

    def load_cabecalhos(self):
        if self.cabecalhos is not None:
            return
        with open(self.filename, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            self.cabecalhos = next(reader)

    def read_filename(self):
        self.dados = []
        self.number_lines = 0
        with open(self.filename, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # pula cabecalho
            for row in reader:
                self.number_lines += 1
                self.dados.append(row)

    def report(self):
        dados_com_rodape = self.dados + [self.cabecalhos]
        print(tabulate(dados_com_rodape, headers=self.cabecalhos, tablefmt="grid"))
        print(f'Planilha com {self.number_lines} linhas e {len(self.cabecalhos)} colunas!')

    def report_with_columns(self, desired_columns):
        colunas_desejadas = [c.strip() for c in desired_columns]
        cabecalhos_limpos = [c.strip() for c in self.cabecalhos]
        indices = [i for i, c in enumerate(cabecalhos_limpos) if c in colunas_desejadas]
        cabecalhos_filtrados = [self.cabecalhos[i] for i in indices]
        dados_filtrados = [[linha[i] for i in indices] for linha in self.dados]
        print(tabulate(dados_filtrados, headers=cabecalhos_filtrados, tablefmt="grid"))
        print(f'Planilha com {self.number_lines} linhas e {len(indices)} colunas selecionadas!')


if '__main__' == __name__:
    filename = os.path.join(os.path.dirname(__file__), '..', 'files', 'cdr.xlsx')
    # filename = '../files/cdr.csv'
    desired_columns = [
        'CdrType',
        'ThingsGroupName',
        'sessionCreationTime',
        'IMSI',
        'Usage',
    ]

    csv = Csv(filename)
    csv.report()
    print('\n--- Colunas selecionadas ---\n')
    csv.report_with_columns(desired_columns)
