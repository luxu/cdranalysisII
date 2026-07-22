import createCrudService from './crud'
import endpoints from './endpoints'

const profileService = createCrudService(endpoints.profile)

export default profileService
