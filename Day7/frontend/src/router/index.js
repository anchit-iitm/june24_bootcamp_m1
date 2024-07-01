import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import register from '@/views/registerview.vue'
import admindashboard from '@/views/admindashboard.vue'

// router.beforeEach

const routes = [
  {
    path: '/',
    name: 'home',
    component: admindashboard
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/login',
    name: 'login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/loginview.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: register
  },
  {
    path: '/addCategory',
    name: 'addCategory',
    component: () => import('@/views/addCategory.vue')
  },
  {
    path: '/addProduct',
    name: 'addProduct',
    component: () => import('@/views/addProduct.vue')
  },
  {
    name: 'updateCategory',
    path: '/updatecategory/:id',
    component: () => import('@/views/updatecategory.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
