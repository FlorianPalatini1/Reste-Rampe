<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Global language selector fixed to top-right (hidden on landing) -->
    <div v-if="routeName !== 'landing'" style="position:fixed;top:8px;right:12px;z-index:60;">
      <LanguageSwitcher />
    </div>
  <!-- Navigation (hidden on landing). Show minimal header on login/register routes -->
  <nav v-if="routeName !== 'landing'" class="bg-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <router-link v-if="routeName !== 'login'" to="/dashboard" class="flex items-center text-lg font-semibold brand-link">
                <img src="/logo-trebuchet.png" alt="Reste Rampe logo" class="h-8 w-8 mr-3" />
                <span>Reste Rampe</span>
              </router-link>
            </div>
            <div v-if="!isMinimalHeader" class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link
                to="/dashboard"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="$route.path === '/dashboard' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                {{ t('nav.overview') }}
              </router-link>
              <router-link
                to="/ingredients"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="$route.path === '/ingredients' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                {{ t('nav.ingredients') }}
              </router-link>
              <router-link
                to="/shopping"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="$route.path === '/shopping' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                {{ t('nav.shopping') }}
              </router-link>
              <router-link
                to="/recipes"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="$route.path === '/recipes' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                {{ t('nav.recipes') }}
              </router-link>
              <router-link
                to="/news"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="$route.path === '/news' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                {{ t('nav.news') }}
              </router-link>
              <router-link
                to="/datenschutz"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="$route.path === '/datenschutz' ? 'border-primary-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'"
              >
                {{ t('nav.privacy') }}
              </router-link>
              <div v-if="isAdmin" class="relative group">
                <button class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium text-gray-500 hover:border-gray-300 hover:text-gray-700">
                  {{ t('nav.admin') }} ▼
                </button>
                <div class="absolute left-0 mt-0 w-48 bg-white rounded-lg shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50">
                  <router-link to="/admin/users" class="block px-4 py-2 hover:bg-gray-100 text-sm">{{ t('nav.manageUsers') }}</router-link>
                  <router-link to="/admin/pages" class="block px-4 py-2 hover:bg-gray-100 text-sm">{{ t('nav.pages') }}</router-link>
                </div>
              </div>
            </div>
          </div>
          <!-- Right: Language Switcher, User info and logout (hidden on minimal header) -->
          <div class="flex items-center space-x-4">
            <div v-if="!isMinimalHeader && isLoggedIn" class="flex items-center space-x-3">
              <div class="flex items-center px-3 py-1 rounded-full bg-gray-100 text-gray-700 text-sm">
                <span class="mr-2 inline-flex h-6 w-6 items-center justify-center rounded-full bg-primary-100 text-primary-700 text-xs font-semibold">
                  {{ initials }}
                </span>
                <span class="font-medium truncate max-w-[12rem]" :title="displayName">{{ displayName }}</span>
              </div>
              <div v-if="isAdmin" class="ml-2">
              </div>
              <button @click="handleLogout"
                class="inline-flex items-center px-3 py-1.5 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
                {{ t('nav.logout') }}
              </button>
            </div>
            <div v-else-if="!isMinimalHeader" class="flex items-center space-x-3">
              <router-link to="/login" class="text-sm text-primary-600 hover:text-primary-700">{{ t('nav.login') }}</router-link>
              <router-link to="/register" class="text-sm text-gray-600 hover:text-gray-800">{{ t('nav.register') }}</router-link>
            </div>
            <!-- when minimal header is active we intentionally show no links on the right side -->
          </div>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main>
      <!-- use a perspective wrapper so the 3D page-turn looks correct -->
      <div class="page-perspective">
        <router-view v-slot="{ Component }">
          <transition :name="transitionName" mode="out-in">
            <div v-if="routeName === 'landing'" key="landing" class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
              <component :is="Component" />
            </div>

            <div v-else key="other" class="paper-root min-h-screen flex flex-col py-6 px-6 bg-paper bg-repeat">
              <div class="flex-1 flex items-start justify-center">
                <div class="w-full max-w-6xl flex items-start justify-center">
                  <div class="content-wrap w-full max-w-5xl mx-6">
                    <component :is="Component" />
                  </div>
                </div>
              </div>
            </div>
          </transition>
        </router-view>
      </div>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-100 border-t border-gray-200 mt-16">
      <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <!-- Branding -->
          <div class="text-center md:text-left">
            <h3 class="text-lg font-semibold text-gray-900">Reste Rampe</h3>
            <p class="mt-2 text-sm text-gray-600">{{ t('app.tagline') || 'Keine Lebensmittel verschwenden' }}</p>
          </div>

          <!-- Legal Links -->
          <div class="text-center">
            <h4 class="text-sm font-semibold text-gray-900 mb-4">{{ t('footer.legal') || 'Rechtliches' }}</h4>
            <nav class="space-y-2">
              <router-link to="/datenschutz" class="block text-sm text-gray-600 hover:text-gray-900">
                {{ t('nav.privacy') }}
              </router-link>
              <router-link to="/impressum" class="block text-sm text-gray-600 hover:text-gray-900">
                {{ t('footer.imprint') || 'Impressum' }}
              </router-link>
              <router-link to="/nutzungsbedingungen" class="block text-sm text-gray-600 hover:text-gray-900">
                {{ t('footer.terms') || 'Nutzungsbedingungen' }}
              </router-link>
              <router-link to="/agb" class="block text-sm text-gray-600 hover:text-gray-900">
                {{ t('footer.agb') || 'AGB' }}
              </router-link>
            </nav>
          </div>

          <!-- Info -->
          <div class="text-center md:text-right">
            <p class="text-sm text-gray-600">© 2025 Reste Rampe. {{ t('footer.allRights') || 'Alle Rechte vorbehalten.' }}</p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuth, loadFromStorage } from './stores/auth'
import LanguageSwitcher from './components/LanguageSwitcher.vue'

const { t } = useI18n()
const { state, logout } = useAuth()
const router = useRouter()

// Load token from localStorage on mount
onMounted(() => {
  loadFromStorage()
})

const isLoggedIn = computed(() => !!state.token)
const isAdmin = computed(() => state.user?.is_admin || false)
const displayName = computed(() => state.user?.username || state.user?.email || 'Guest')
const initials = computed(() => {
  const name = state.user?.username || state.user?.email || ''
  if (!name) return '?'
  const parts = String(name).split(/\s|\./).filter(Boolean)
  const chars = parts.length >= 2 ? parts[0][0] + parts[1][0] : name.slice(0, 2)
  return chars.toUpperCase()
})

// route-aware helpers
import { useRoute } from 'vue-router'
const route = useRoute()
const routeName = computed(() => route.name)

// transition selection: if navigating between landing and login use a page-turn
const transitionName = ref('fade')

// watch route changes to pick a transition
watch(route, (to, from) => {
  const fromName = String(from.name || '')
  const toName = String(to.name || '')
  // if navigating between landing and login, use page-turn animation
  if ((fromName === 'landing' && toName === 'login') || (fromName === 'login' && toName === 'landing')) {
    // forward if going landing -> login, back otherwise
    transitionName.value = (fromName === 'landing' && toName === 'login') ? 'page-turn-forward' : 'page-turn-back'
  } else {
    transitionName.value = 'fade'
  }
}, { immediate: true })
// when on login or register show a minimal header (only brand)
const isMinimalHeader = computed(() => {
  const name = String(route.name || '')
  // Show minimal header on auth pages and legal pages
  return name === 'login' || name === 'register' || 
         name === 'privacy' || name === 'imprint' || name === 'terms' || name === 'agb'
})

function handleLogout() {
  logout()
  router.push({ name: 'login' })
}

// reactive state for admin help modal
const showAdminHelp = ref(false)
const adminTokenInput = ref('')

function setTokenFromInput() {
  if (!adminTokenInput.value || adminTokenInput.value.length < 20) {
    alert('Please paste a valid token')
    return
  }
  localStorage.setItem('token', adminTokenInput.value.trim())
  // reload so auth store picks up the token
  location.reload()
}
</script>

<style scoped>
/* Reuse the paper/masthead styles for non-landing pages */
.paper-root { background-color: #f7f3ee; background-image: linear-gradient(rgba(0,0,0,0.02) 1px, transparent 1px); background-size: 100% 26px; }
.masthead-hero { font-size: 4.75rem; line-height: 1; margin: 0; color: #1a1a1a; letter-spacing: -0.02em; text-transform: uppercase; font-weight: 700; font-family: 'Playfair Display', Georgia, 'Times New Roman', serif; }
.masthead-sub { margin-top: 0.5rem; color: #5a4f43; font-size: 1.125rem; text-decoration: underline; text-underline-offset: 6px; }
.content-wrap { background: linear-gradient(180deg, #fffdf9 0%, #fbf7f1 100%); border: 1px solid #e6ded2; box-shadow: 0 10px 30px rgba(30,20,10,0.04); padding: 2rem; }
.brand-link { color: #5a3826; display:inline-flex; align-items:center; gap:0.5rem; }

/* Page-turn transition styles */
.page-perspective { perspective: 1200px; }

/* fallback fade */
.fade-enter-active, .fade-leave-active { transition: opacity .35s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* forward page turn (landing -> login) */
.page-turn-forward-enter-active, .page-turn-forward-leave-active {
  /* much slower, more pronounced flip */
  transition: transform 1.6s cubic-bezier(0.18, 0.8, 0.22, 1), opacity .55s ease;
  transform-origin: left center;
}
.page-turn-forward-enter-from { transform: rotateY(120deg) translateX(40%); opacity: 0; }
.page-turn-forward-enter-to   { transform: rotateY(0deg) translateX(0); opacity: 1; }
.page-turn-forward-leave-from { transform: rotateY(0deg) translateX(0); opacity: 1; }
.page-turn-forward-leave-to   { transform: rotateY(-120deg) translateX(-40%); opacity: 0; }

/* back page turn (login -> landing) - invert rotation origin */
.page-turn-back-enter-active, .page-turn-back-leave-active {
  transition: transform 1.6s cubic-bezier(0.18, 0.8, 0.22, 1), opacity .55s ease;
  transform-origin: right center;
}
.page-turn-back-enter-from { transform: rotateY(-120deg) translateX(-40%); opacity: 0; }
.page-turn-back-enter-to   { transform: rotateY(0deg) translateX(0); opacity: 1; }
.page-turn-back-leave-from { transform: rotateY(0deg) translateX(0); opacity: 1; }
.page-turn-back-leave-to   { transform: rotateY(120deg) translateX(40%); opacity: 0; }

/* stronger shadow and visible paper edge to emphasize the flip */
.page-perspective { -webkit-perspective: 1600px; perspective: 1600px; }
.page-perspective > * {
  position: relative; /* allow ::before edge */
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  transform-style: preserve-3d;
  -webkit-transform-style: preserve-3d;
  box-shadow: 0 28px 90px rgba(0,0,0,0.36);
  transition: box-shadow .4s ease;
}

/* thick, darker paper edge gradient (left edge) to give a newspaper look */
.page-perspective > *::before {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: 18px;
  pointer-events: none;
  background: linear-gradient(90deg, rgba(0,0,0,0.42), rgba(0,0,0,0.18) 30%, rgba(255,255,255,0) 70%);
  border-top-right-radius: 3px;
  border-bottom-right-radius: 3px;
  opacity: 1;
  transform-origin: left center;
  transform: translateZ(1px) scaleX(1);
  transition: transform .45s cubic-bezier(.2,.9,.2,1), opacity .45s ease;
}

/* animate edge during enter/leave to mimic page curl */
.page-turn-forward-enter-from > *::before,
.page-turn-back-enter-from > *::before {
  transform: translateZ(1px) scaleX(0.2);
  opacity: 0.0;
}
.page-turn-forward-enter-to > *::before,
.page-turn-back-enter-to > *::before {
  transform: translateZ(1px) scaleX(1);
  opacity: 1;
}

/* reduce edge opacity when centered */
.page-perspective > *.page-focused::before { opacity: 0.55; transform: translateZ(1px) scaleX(.85); }
</style>

