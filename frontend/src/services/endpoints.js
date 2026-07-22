// Mapa central dos endpoints da API (convenção DRF Router, plural).
// Se o backend usar caminhos diferentes, ajuste aqui em uma linha por entidade.
const endpoints = {
  organization: '/organizations/',
  customer: '/customers/',
  mno: '/mnos/',
  networkprovider: '/networkproviders/',
  priceplan: '/priceplans/',
  thing: '/things/',
  device: '/devices/',
  session: '/sessions/',
  profile: '/profiles/',
  user: '/users/'
}

export default endpoints
