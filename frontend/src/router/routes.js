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
      { path: '', component: () => import('@/pages/PanelPage.vue') },
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
        path: 'xlsx',
        name: 'xlsx',
        component: () => import('@/pages/LoadPage.vue')
      }
    ]
  },

  {
    path: '/admin',
    meta: { requiresStaff: true },
    component: () => import('@/layouts/AdminLayout.vue'),
    children: [
      {
        path: '',
        name: 'admin',
        component: () => import('@/pages/AdminPage.vue')
      },
      {
        path: 'thing',
        name: 'admin-thing',
        component: () => import('@/pages/thing/ListPage.vue')
      },
      {
        path: 'thing-form/:id?',
        name: 'admin-form-thing',
        component: () => import('@/pages/thing/FormPage.vue'),
        meta: { listRoute: '/admin/thing' }
      },
      {
        path: 'profile',
        name: 'admin-profile',
        component: () => import('@/pages/profile/ListPage.vue')
      },
      {
        path: 'profile-form/:id?',
        name: 'admin-form-profile',
        component: () => import('@/pages/profile/FormPage.vue'),
        meta: { listRoute: '/admin/profile' }
      }
    ]
  },

  {
    path: '/:catchAll(.*)*',
    component: () => import('@/pages/ErrorNotFound.vue')
  }
]

export default routes
