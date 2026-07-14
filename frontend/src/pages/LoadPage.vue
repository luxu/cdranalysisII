<template>
  <q-page padding class="q-gutter-y-md">
    <div class="row q-col-gutter-md justify-center">
      
      <div class="col-12 col-md-8">
        <q-card class="my-card q-pa-md">
          <q-card-section>
            <div class="text-h6 q-mb-md">Upload de Arquivo</div>
            
            <q-file
              v-model="arquivo"
              label="Selecione ou arraste um arquivo Excel (.xlsx)"
              outlined
              append
              counter
              :max-files="1"
              accept=".xlsx, .xls"
              @rejected="onRejected"
            >
              <template v-slot:prepend>
                <q-icon name="attach_file" />
              </template>

              <template v-slot:append>
                <q-icon
                  v-if="arquivo"
                  name="close"
                  @click.stop.prevent="limparDados"
                  class="cursor-pointer"
                />
              </template>
            </q-file>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn
              label="Visualizar Dados"
              color="primary"
              :disable="!arquivo"
              @click="lerEVisualizarArquivo"
            />
          </q-card-actions>
        </q-card>
      </div>

      <div v-if="linhasTabela.length > 0" class="col-12 col-md-10">
        <q-card class="my-card q-pa-md">
          <q-card-section>
            <div class="text-h6 q-mb-md">Dados Originais: {{ arquivo?.name }}</div>
            
            <q-table
              flat
              bordered
              :rows="linhasTabela"
              :columns="colunasTabela"
              row-key="id"
              :pagination="{ rowsPerPage: 5 }"
            />
          </q-card-section>

          <q-card-section class="bg-grey-2 q-mt-md rounded-borders">
            <div class="text-subtitle1 q-mb-sm text-weight-bold">Filtrar Colunas</div>
            <q-select
              v-model="colunasSelecionadas"
              multiple
              outlined
              dense
              options-sanitize
              :options="opcoesColunas"
              label="Selecione as colunas para exportar/filtrar"
              use-chips
              stack-label
              class="bg-white"
            />
          </q-card-section>
        </q-card>
      </div>

      <div v-if="colunasSelecionadas.length > 0" class="col-12 col-md-10">
        <q-card class="my-card q-pa-md border-filtered">
          <q-card-section>
            <div class="text-h6 text-secondary q-mb-md flex items-center">
              <q-icon name="filter_alt" class="q-mr-sm" />
              Dados Filtrados
            </div>
            
            <q-table
              flat
              bordered
              :rows="linhasFiltradas"
              :columns="colunasFiltradas"
              row-key="id"
              :pagination="{ rowsPerPage: 5 }"
            />
          </q-card-section>
        </q-card>
      </div>

    </div>
  </q-page>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useQuasar } from 'quasar'
import * as XLSX from 'xlsx'

const $q = useQuasar()
const arquivo = ref(null)

// Estados da Tabela Principal
const linhasTabela = ref([])
const colunasTabela = ref([])

// Estado do Filtro (guarda os objetos das colunas escolhidas)
const colunasSelecionadas = ref([])

// Computado para alimentar as opções do q-select (transforma as colunas em label/value)
const opcoesColunas = computed(() => {
  return colunasTabela.value.map(col => ({
    label: col.label,
    value: col.name
  }))
})

// Computado que monta dinamicamente as colunas da SEGUNDA tabela
const colunasFiltradas = computed(() => {
  const chavesSelecionadas = colunasSelecionadas.value.map(opt => opt.value)
  return colunasTabela.value.filter(col => chavesSelecionadas.includes(col.name))
})

// Computado que filtra os dados das linhas para a SEGUNDA tabela
const linhasFiltradas = computed(() => {
  const chavesSelecionadas = colunasSelecionadas.value.map(opt => opt.value)
  
  return linhasTabela.value.map(linha => {
    // Começa apenas com o ID para manter a reatividade da linha no q-table
    const novaLinha = { id: linha.id }
    // Copia apenas as propriedades das colunas que foram selecionadas
    chavesSelecionadas.forEach(chave => {
      novaLinha[chave] = linha[chave]
    })
    return novaLinha
  })
})

const lerEVisualizarArquivo = () => {
  if (!arquivo.value) return

  $q.loading.show({ message: 'Processando planilha...' })

  const reader = new FileReader()

  reader.onload = (e) => {
    try {
      const data = new Uint8Array(e.target.result)
      const workbook = XLSX.read(data, { type: 'array' })
      const primeiraAbaNome = workbook.SheetNames[0]
      const aba = workbook.Sheets[primeiraAbaNome]
      const dadosJson = XLSX.utils.sheet_to_json(aba, { header: 1 })

      if (dadosJson.length > 0) {
        const cabecalhos = dadosJson[0]
        
        // Monta colunas originais
        colunasTabela.value = cabecalhos.map((label, index) => ({
          name: `col_${index}`,
          label: label,
          field: `col_${index}`,
          align: 'left',
          sortable: true
        }))

        // Monta linhas originais
        linhasTabela.value = dadosJson.slice(1).map((linha, indexLinha) => {
          const objetoLinha = { id: indexLinha }
          cabecalhos.forEach((_, indexCol) => {
            objetoLinha[`col_${indexCol}`] = linha[indexCol] !== undefined ? linha[indexCol] : ''
          })
          return objetoLinha
        })

        // Limpa seleções anteriores caso troque de arquivo
        colunasSelecionadas.value = []

        $q.notify({ type: 'positive', message: 'Dados carregados!' })
      }
    } catch (error) {
      $q.notify({ type: 'negative', message: 'Erro ao ler arquivo.' })
    } finally {
      $q.loading.hide()
    }
  }

  reader.readAsArrayBuffer(arquivo.value)
}

const limparDados = () => {
  arquivo.value = null
  linhasTabela.value = []
  colunasTabela.value = []
  colunasSelecionadas.value = []
}

const onRejected = () => {
  $q.notify({ type: 'warning', message: 'Formato inválido.' })
}
</script>

<style scoped>
.my-card {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}
.border-filtered {
  border-top: 4px solid var(--q-secondary);
}
</style>