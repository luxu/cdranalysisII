import createCrudService from './crud'
import endpoints from './endpoints'

const sessionService = createCrudService(endpoints.session)

export default sessionService
