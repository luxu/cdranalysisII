import createCrudService from './crud'
import endpoints from './endpoints'

const userService = createCrudService(endpoints.user)

export default userService
