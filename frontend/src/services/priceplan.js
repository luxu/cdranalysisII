import createCrudService from './crud'
import endpoints from './endpoints'

const priceplanService = createCrudService(endpoints.priceplan)

export default priceplanService
