<template>
  <div class="paper-root min-h-screen flex flex-col py-6 px-6 bg-paper bg-repeat">
    <!-- Masthead -->
    <header class="w-full max-w-6xl text-center mb-4 mx-auto">
      <h1 class="masthead-hero">{{ t('app.title') }}</h1>
      <p class="masthead-sub">Reste Rampe — Die Zeitung für nachhaltiges Kochen</p>
    </header>

    <div class="flex-1 flex items-center justify-center">
      <div class="w-full max-w-6xl flex items-center justify-center">
        <div class="login-card p-12 bg-white/96 border border-gray-200 shadow-2xl max-w-2xl w-full mx-6">
          <!-- Verifying -->
          <div v-if="verifying" class="text-center">
            <h2 class="text-3xl font-serif mb-6">{{ t('verify.title', 'Email wird überprüft...') }}</h2>
            <div class="inline-block">
              <div class="inline-flex items-center justify-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
              </div>
            </div>
            <p class="text-gray-600 mt-4">{{ t('verify.checking', 'Bitte warten...') }}</p>
          </div>

          <!-- Success -->
          <div v-else-if="success" class="text-center">
            <div class="mb-6">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
                <svg class="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
              </div>
              <h2 class="text-3xl font-serif mb-4">{{ t('verify.success', 'Email bestätigt!') }}</h2>
              <p class="text-gray-700 mb-6">
                {{ t('verify.successMessage', 'Dein Konto wurde erfolgreich aktiviert. Du wirst in Kürze zum Login weitergeleitet...') }}
              </p>
            </div>
          </div>

          <!-- Error -->
          <div v-else-if="error" class="text-center">
            <div class="mb-6">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-red-100 rounded-full mb-4">
                <svg class="w-8 h-8 text-red-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                </svg>
              </div>
              <h2 class="text-3xl font-serif mb-4">{{ t('verify.error', 'Fehler') }}</h2>
              <p class="text-red-700 mb-6">{{ errorMsg }}</p>
            </div>
            <router-link to="/register" class="inline-block bg-black text-white px-8 py-3 rounded-sm text-lg font-medium hover:bg-gray-800 transition">
              {{ t('verify.backToRegister', 'Zurück zur Registrierung') }}
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import api from '../lib/api'
import { useAuth } from '../stores/auth'

const { t } = useI18n()
const { setToken } = useAuth()
const route = useRoute()
const router = useRouter()

const verifying = ref(true)
const success = ref(false)
const error = ref(false)
const errorMsg = ref('')

onMounted(async () => {
  const token = route.query.token

  if (!token) {
    errorMsg.value = t('verify.noToken', 'Kein Verifikations-Token vorhanden')
    error.value = true
    verifying.value = false
    return
  }

  try {
    const resp = await api.post('/auth/verify-email', { token })
    
    if (resp && resp.data && resp.data.access_token) {
      setToken(resp.data.access_token)
      success.value = true
      
      // Redirect to dashboard after 2 seconds
      setTimeout(() => {
        router.push({ name: 'dashboard' })
      }, 2000)
    } else {
      errorMsg.value = t('verify.failed', 'Verifizierung fehlgeschlagen')
      error.value = true
    }
  } catch (err) {
    console.error('Verification error:', err)
    errorMsg.value = err?.response?.data?.detail || t('verify.failed', 'Verifizierung fehlgeschlagen')
    error.value = true
  } finally {
    verifying.value = false
  }
})
</script>

<style scoped>
.paper-root { background-color: #f7f3ee; background-image: url("data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'%3E%3Crect width='200' height='200' fill='%23f7f3ee'/%3E%3Cg opacity='0.06' fill='%23000000'%3E%3Ccircle cx='10' cy='20' r='0.6'/%3E%3Ccircle cx='40' cy='80' r='0.6'/%3E%3Ccircle cx='70' cy='30' r='0.6'/%3E%3Ccircle cx='120' cy='140' r='0.6'/%3E%3Ccircle cx='160' cy='60' r='0.6'/%3E%3Ccircle cx='190' cy='180' r='0.6'/%3E%3C/g%3E%3C/svg%3E"); background-repeat: repeat; background-size: 200px 200px; }
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&display=swap');
.masthead { font-family: 'Playfair Display', Georgia, 'Times New Roman', serif; color: #0b1720; letter-spacing: -0.02em; }

@keyframes spin {
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
