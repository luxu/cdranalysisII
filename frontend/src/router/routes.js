const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/pages/LoginPage.vue')
  },
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('@/pages/IndexPage.vue') },
      {
        path: 'profile',
        name: 'profile',
        component: () => import('@/pages/profile/ListPage.vue')
      },
      {
        path: 'profile-form/:id?',
        name: 'form-profile',
        component: () => import('@/pages/profile/FormPage.vue')
      },
      {
        path: 'device',
        name: 'device',
        component: () => import('@/pages/device/ListPage.vue')
      },
      {
        path: 'device-form/:id?',
        name: 'form-device',
        component: () => import('@/pages/device/FormPage.vue')
      },
      {
        path: 'organization',
        name: 'organization',
        component: () => import('@/pages/organization/ListPage.vue')
      },
      {
        path: 'organization-form/:id?',
        name: 'form-organization',
        component: () => import('@/pages/organization/FormPage.vue')
      },
      {
        path: 'customer',
        name: 'customer',
        component: () => import('@/pages/customer/ListPage.vue')
      },
      {
        path: 'customer-form/:id?',
        name: 'form-customer',
        component: () => import('@/pages/customer/FormPage.vue')
      },
      {
        path: 'mno',
        name: 'mno',
        component: () => import('@/pages/mno/ListPage.vue')
      },
      {
        path: 'mno-form/:id?',
        name: 'form-mno',
        component: () => import('@/pages/mno/FormPage.vue')
      },
      {
        path: 'networkprovider',
        name: 'networkprovider',
        component: () => import('@/pages/networkprovider/ListPage.vue')
      },
      {
        path: 'networkprovider-form/:id?',
        name: 'form-networkprovider',
        component: () => import('@/pages/networkprovider/FormPage.vue')
      },
      {
        path: 'priceplan',
        name: 'priceplan',
        component: () => import('@/pages/priceplan/ListPage.vue')
      },
      {
        path: 'priceplan-form/:id?',
        name: 'form-priceplan',
        component: () => import('@/pages/priceplan/FormPage.vue')
      },
      {
        path: 'thing',
        name: 'thing',
        component: () => import('@/pages/thing/ListPage.vue')
      },
      {
        path: 'thing-form/:id?',
        name: 'form-thing',
        component: () => import('@/pages/thing/FormPage.vue')
      },
      {
        path: 'session',
        name: 'session',
        component: () => import('@/pages/session/ListPage.vue')
      },
      {
        path: 'session-form/:id?',
        name: 'form-session',
        component: () => import('@/pages/session/FormPage.vue')
      },
      {
        path: 'xlsx',
        name: 'xlsx',
        component: () => import('@/pages/LoadPage.vue')
      }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('@/pages/ErrorNotFound.vue')
  }
]

export default routes
