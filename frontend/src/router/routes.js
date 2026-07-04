const routes = [
  {
    path: '/',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('@/pages/IndexPage.vue') },
      { path: 'profile', name: 'profile', component: () => import('@/pages/profile/ListPage.vue') },
      { path: 'profile-form/:id?', name: 'form-profile', component: () => import('@/pages/profile/FormPage.vue') }
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
