<template>
  <div class="paper-root min-h-screen flex flex-col py-6 px-6 bg-paper bg-repeat">
    <header class="w-full max-w-6xl text-center mb-4 mx-auto">
      <h1 class="masthead-hero">{{ t('app.title') }}</h1>
      <p class="masthead-sub">Reste Rampe — Die Zeitung für nachhaltiges Kochen</p>
    </header>

    <div class="flex-1 flex items-center justify-center">
      <div class="w-full max-w-6xl flex items-center justify-center">
        <div class="login-card p-12 bg-white/96 border border-gray-200 shadow-2xl max-w-2xl w-full mx-6">
          <div v-if="!registrationComplete">
            <h2 class="text-4xl md:text-5xl font-serif mb-6 text-center">{{ t('register.title') }}</h2>
            <form @submit.prevent="onSubmit" class="space-y-5">
              <div v-if="errorMsg" class="p-4 bg-red-100 border border-red-400 text-red-700 rounded-sm mb-4">
                {{ errorMsg }}
              </div>
              <div>
                <label class="block text-sm font-semibold mb-2">{{ t('register.email') }}</label>
                <input v-model="email" type="email" required :placeholder="t('register.email')" class="w-full p-4 text-lg border border-gray-300 rounded-sm" />
              </div>
              <div>
                <label class="block text-sm font-semibold mb-2">{{ t('register.username') }}</label>
                <input v-model="username" required :placeholder="t('register.username')" class="w-full p-4 text-lg border border-gray-300 rounded-sm" />
              </div>
              <div>
                <label class="block text-sm font-semibold mb-2">{{ t('register.password') }}</label>
                <input v-model="password" type="password" required :placeholder="t('register.password')" class="w-full p-4 text-lg border border-gray-300 rounded-sm" />
              </div>
              <div class="flex justify-center">
                <button :disabled="loading" class="bg-black text-white px-8 py-3 rounded-sm text-lg font-medium disabled:opacity-50">
                  {{ loading ? t('common.loading') : t('register.submit') }}
                </button>
              </div>
            </form>
            <p class="mt-6 text-center text-sm text-gray-700">{{ t('register.hasAccount') }} <router-link to="/login" class="underline">{{ t('register.login') }}</router-link></p>
          </div>

          <div v-else class="text-center">
            <div class="mb-6">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
                <svg class="w-8 h-8 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
              </div>
              <h2 class="text-3xl font-serif mb-4">Email bestätigen</h2>
              <p class="text-gray-700 mb-4">Wir haben eine Bestätigungsemail an {{ registeredEmail }} gesendet.</p>
              <p class="text-sm text-gray-600 mb-6">Bitte überprüfe deinen Spam-Ordner, falls du die Email nicht sehen kannst.</p>
            </div>

            <div class="bg-blue-50 border border-blue-200 rounded-sm p-4 mb-6">
              <p class="text-sm text-blue-800"><strong>💡 Tipp:</strong> Nach der Email-Bestätigung kannst du dich sofort anmelden.</p>
            </div>

            <router-link to="/login" class="inline-block bg-black text-white px-8 py-3 rounded-sm text-lg font-medium hover:bg-gray-800 transition">
              Zurück zum Login
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import api from '../lib/api'
import { useI18n } from 'vue-i18n'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const { t } = useI18n()
const email = ref('')
const username = ref('')
const password = ref('')
const router = useRouter()
const loading = ref(false)
const errorMsg = ref('')
const registrationComplete = ref(false)
const registeredEmail = ref('')

async function onSubmit() {
  if (!email.value || !username.value || !password.value) {
    errorMsg.value = t('register.error')
    return
  }

  loading.value = true
  errorMsg.value = ''

  try {
    const resp = await api.post('/auth/register', { 
      email: email.value, 
      username: username.value, 
      password: password.value 
    })
    
    if (resp && resp.data && resp.data.email) {
      registeredEmail.value = resp.data.email
      registrationComplete.value = true
    } else {
      errorMsg.value = t('register.error')
    }
  } catch (err) {
    const msg = err?.response?.data?.detail || err?.message || t('register.error')
    errorMsg.value = msg
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.paper-root { background-color: #f7f3ee; background-image: url("data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'%3E%3Crect width='200' height='200' fill='%23f7f3ee'/%3E%3Cg opacity='0.06' fill='%23000000'%3E%3Ccircle cx='10' cy='20' r='0.6'/%3E%3Ccircle cx='40' cy='80' r='0.6'/%3E%3Ccircle cx='70' cy='30' r='0.6'/%3E%3Ccircle cx='120' cy='140' r='0.6'/%3E%3Ccircle cx='160' cy='60' r='0.6'/%3E%3Ccircle cx='190' cy='180' r='0.6'/%3E%3C/g%3E%3C/svg%3E"); background-repeat: repeat; background-size: 200px 200px; }
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&display=swap');
.masthead { font-family: 'Playfair Display', Georgia, 'Times New Roman', serif; color: #0b1720; letter-spacing: -0.02em; }
</style>
