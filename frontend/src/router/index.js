import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Ingredients from '../views/Ingredients.vue'
import ShoppingLists from '../views/ShoppingLists.vue'
import Recipes from '../views/Recipes.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import News from '../views/News.vue'
import NewsDetail from '../views/NewsDetail.vue'
import Privacy from '../views/Privacy.vue'
import AdminUsers from '../views/AdminUsers.vue'
import AdminPages from '../views/AdminPages.vue'
import LandingAnimation from '../views/LandingAnimation.vue'
import { getToken, useAuth } from '../stores/auth'
import api from '../lib/api'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'root-redirect',
      redirect: { name: 'landing' }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard
    },
    {
      path: '/ingredients',
      name: 'ingredients',
      component: Ingredients
    },
    {
      path: '/shopping',
      name: 'shopping',
      component: ShoppingLists
    },
    {
      path: '/recipes',
      name: 'recipes',
      component: Recipes
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/news',
      name: 'news',
      component: News
    },
    {
      path: '/news/:slug',
      name: 'news-detail',
      component: NewsDetail
    },
    {
      path: '/datenschutz',
      name: 'privacy',
      component: Privacy
    },
    {
      path: '/impressum',
      name: 'imprint',
      component: Privacy
    },
    {
      path: '/nutzungsbedingungen',
      name: 'terms',
      component: Privacy
    },
    {
      path: '/agb',
      name: 'agb',
      component: Privacy
    },
    {
      path: '/admin/users',
      name: 'admin-users',
      component: AdminUsers,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin/pages',
      name: 'admin-pages',
      component: AdminPages,
      meta: { requiresAuth: true, requiresAdmin: true }
    },
    {
      path: '/admin',
      name: 'admin',
      redirect: { name: 'admin-users' }
    },
    {
      path: '/landing',
      name: 'landing',
      component: LandingAnimation
    },
    // keep old admin paths working by redirecting to the consolidated admin page
    {
      path: '/admin/users',
      redirect: { name: 'admin' }
    },
    {
      path: '/admin/news',
      redirect: { name: 'admin' }
    },
    {
      path: '/admin/pages',
      redirect: { name: 'admin' }
    }
  ]
})

// simple global guard: redirect to /login if route is protected and no token
router.beforeEach(async (to, from, next) => {
  const publicPages = ['login', 'register', 'news', 'news-detail', 'privacy', 'imprint', 'terms', 'agb', 'landing', 'landing-root']
  const { state, setToken } = useAuth()
  if (publicPages.includes(to.name)) return next()

  const token = getToken()
  if (!token) return next({ name: 'login' })

  // if we already loaded user, allow navigation
  if (state.user) {
    // Check admin route
    if (to.meta.requiresAdmin && !state.user.is_admin) {
      return next({ name: 'dashboard' })
    }
    return next()
  }

  // attempt to validate token with backend
  try {
    const resp = await api.get('/auth/me')
    state.user = resp.data
    
    // Check admin route
    if (to.meta.requiresAdmin && !resp.data.is_admin) {
      return next({ name: 'dashboard' })
    }
    
    return next()
  } catch (err) {
    // invalid token
    setToken(null)
    return next({ name: 'login' })
  }
})

export default router
