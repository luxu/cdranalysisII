import createCrudService from './crud'
import endpoints from './endpoints'

const deviceService = createCrudService(endpoints.device)

export default deviceService
