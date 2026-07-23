import { api } from '@/boot/axios'

const cdrImportService = {
  async upload(file) {
    const formData = new FormData()
    formData.append('file', file)
    const { data } = await api.post('/sessions/import-cdr/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return data
  }
}

export default cdrImportService
