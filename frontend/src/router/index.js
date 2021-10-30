import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

let opts = {
  routes: [
    {
      path: "/",
      name: "Index",
      redirect: "/dashboard",
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/dashboard",
      name: "Dashboard",
      component: () => import('../views/Dashboard.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/camera",
      name: "Camera",
      component: () => import('../views/Camera.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/violations",
      name: "Violation",
      component: () => import('../views/ViolationsTable.vue'),
      meta: {
        requiresAuth: true
      },
      children: [
        {
          path: "photo/:id",
          name: "ViolationPhoto",
          component: () => import('../components/modals/ViolationModal.vue'),
          meta: {
            requiresAuth: true
          },
        },
      ]
    },
    {
      path: "/login",
      name: "login",
      component: () => import('../views/Login.vue'),
      meta: {
        requiresAuth: false
      }
    },
  ],
  linkExactActiveClass: 'active'
};
const router = new VueRouter(opts);

export default router
