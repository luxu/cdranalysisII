import createCrudService from './crud'
import endpoints from './endpoints'

const customerService = createCrudService(endpoints.customer)

export default customerService
