import createCrudService from './crud'
import endpoints from './endpoints'

const organizationService = createCrudService(endpoints.organization)

export default organizationService
