import createCrudService from './crud'
import endpoints from './endpoints'

const mnoService = createCrudService(endpoints.mno)

export default mnoService
