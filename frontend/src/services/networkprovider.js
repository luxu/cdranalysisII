import createCrudService from './crud'
import endpoints from './endpoints'

const networkproviderService = createCrudService(endpoints.networkprovider)

export default networkproviderService
