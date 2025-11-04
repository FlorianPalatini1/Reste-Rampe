<template>
  <div class="paper-root min-h-screen flex flex-col py-6 px-6 bg-paper bg-repeat">
    <header class="w-full max-w-6xl mb-4 mx-auto">
      <div class="text-center">
        <div class="masthead-with-logo inline-flex items-center justify-center">
          <img src="/logo-trebuchet.png" alt="Reste Rampe logo" class="masthead-logo" />
          <h1 class="masthead-hero">Reste Rampe</h1>
        </div>
        <p class="masthead-sub">Die interaktive "Zeitung" für nachhaltiges Kochen</p>
      </div>
    </header>

    <div class="flex-1 flex items-start justify-center pt-12 lg:pt-8">
      <div class="w-full max-w-6xl flex items-start justify-center">
        <div class="login-card p-12 bg-white/96 border border-gray-200 shadow-2xl max-w-2xl w-full mx-6">
          <h2 class="text-4xl md:text-5xl font-serif mb-6 text-center">{{ t('login.title') }}</h2>

          <form @submit.prevent="onSubmit" class="space-y-5">
            <div v-if="errorMsg" class="p-4 bg-red-100 border border-red-400 text-red-700 rounded-sm mb-4">
              {{ errorMsg }}
            </div>
            <div>
              <label class="block text-sm font-semibold mb-2">{{ t('login.username') }}</label>
              <input v-model="email" :placeholder="t('login.username')" class="w-full p-4 text-lg border border-gray-300 rounded-sm" />
            </div>
            <div>
              <label class="block text-sm font-semibold mb-2">{{ t('login.password') }}</label>
              <input v-model="password" type="password" :placeholder="t('login.password')" class="w-full p-4 text-lg border border-gray-300 rounded-sm" />
            </div>
            <div class="flex justify-center">
              <button :disabled="loading" class="bg-black text-white px-8 py-3 rounded-sm text-lg font-medium disabled:opacity-50">
                {{ loading ? t('common.loading') : t('login.submit') }}
              </button>
            </div>
          </form>

          <p class="mt-6 text-center text-sm text-gray-700">{{ t('login.noAccount') }} <router-link to="/register" class="underline">{{ t('login.register') }}</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import api from '../lib/api'
import { useAuth } from '../stores/auth'

export default {
  name: 'LoginView',
  setup() {
    const email = ref('')
    const password = ref('')
    const router = useRouter()
    const { setToken } = useAuth()
    const { t } = useI18n()
    const loading = ref(false)
    const errorMsg = ref('')

    async function onSubmit() {
      if (!email.value || !password.value) {
        errorMsg.value = t('login.error')
        return
      }

      loading.value = true
      errorMsg.value = ''

      try {
        console.log('Attempting login with username:', email.value)
        const resp = await api.post('/auth/login', { 
          username: email.value, 
          password: password.value 
        })
        
        console.log('Login response:', resp.data)
        
        if (resp && resp.data && resp.data.access_token) {
          console.log('Token received, setting token...')
          setToken(resp.data.access_token)
          console.log('Token set, navigating to dashboard...')
          // navigate directly to dashboard
          await router.push({ name: 'dashboard' })
        } else {
          errorMsg.value = t('login.error')
        }
      } catch (err) {
        console.error('Login error:', err)
        const msg = err?.response?.data?.detail || err?.message || t('login.error')
        errorMsg.value = msg
        alert(msg)
      } finally {
        loading.value = false
      }
    }

    return { email, password, onSubmit, t, loading, errorMsg }
  }
}
</script>

<style scoped>
.paper-root { background-color: #f7f3ee; background-image: linear-gradient(rgba(0,0,0,0.02) 1px, transparent 1px); background-size: 100% 26px; }
.masthead-hero {
  font-size: 4.75rem;
  line-height: 1;
  margin: 0;
  color: #1a1a1a;
  /* nudge the masthead slightly upward so it visually aligns with the login card */
  margin-top: -18px;
  transform: translateY(-6px);
}

.masthead-with-logo { gap: 0.125rem; align-items:baseline; }
/* Make the logo roughly the same visual height as the masthead and nudge it further left */
.masthead-logo { height: 110px; width: 110px; object-fit:contain; display:inline-block; transform: translateX(-24px); }

@media (max-width: 1024px) {
  .masthead-hero {
    font-size: 3.75rem;
    margin-top: -12px;
    transform: translateY(-4px);
  }
  .masthead-logo { height:84px; width:84px; transform: translateX(-18px); }
}

@media (max-width: 480px) {
  .masthead-hero {
    font-size: 2.25rem;
    margin-top: -8px;
    transform: translateY(-2px);
  }
  .masthead-with-logo { display:flex; flex-direction:column; gap:0.25rem; }
  .masthead-logo { height:46px; width:46px; transform: translateX(-10px); }
}

.login-card { background: rgba(255,255,255,0.98); border-radius: 6px; }
</style>
