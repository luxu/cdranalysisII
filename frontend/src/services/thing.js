import createCrudService from './crud'
import endpoints from './endpoints'

const thingService = createCrudService(endpoints.thing)

export default thingService
