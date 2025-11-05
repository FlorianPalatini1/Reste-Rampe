<template>
  <div class="paper-root min-h-screen flex flex-col py-6 px-6 bg-paper bg-repeat">
    <!-- Header -->
    <header class="w-full max-w-6xl mb-4 mx-auto">
      <div class="text-center">
        <div class="masthead-with-logo inline-flex items-center justify-center">
          <img src="/logo-trebuchet.png" alt="Reste Rampe logo" class="masthead-logo" />
          <h1 class="masthead-hero">{{ $t('nav.mailbox') }}</h1>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div class="flex-1 flex items-start justify-center pt-8">
      <div class="w-full max-w-4xl">
        <!-- Loading State -->
        <div v-if="loading" class="text-center py-12">
          <div class="spinner mx-auto mb-4"></div>
          <p>{{ $t('common.loading') }}</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
          <p class="font-bold">{{ $t('common.error') }}</p>
          <p>{{ error }}</p>
          <button @click="loadMailboxStatus" class="mt-3 bg-red-500 hover:bg-red-700 text-white px-3 py-1 rounded">
            {{ $t('common.retry') }}
          </button>
        </div>

        <!-- No Mailbox State -->
        <div v-else-if="!mailboxStatus.enabled" class="bg-white rounded-lg shadow-lg p-8">
          <div class="text-center">
            <svg class="w-16 h-16 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
            <h2 class="text-2xl font-bold mb-2 text-gray-800">{{ $t('mailbox.noMailbox') }}</h2>
            <p class="text-gray-600 mb-6">{{ $t('mailbox.createMailboxDesc') }}</p>

            <!-- Create Mailbox Form -->
            <div class="bg-gray-50 rounded-lg p-6 mb-6">
              <form @submit.prevent="createMailbox">
                <div class="mb-4">
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ $t('mailbox.emailAddress') }}
                  </label>
                  <input
                    type="text"
                    disabled
                    :value="`${extractUsername(mailboxStatus.email)}@reste-rampe.tech`"
                    class="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-100 cursor-not-allowed"
                  />
                  <p class="text-xs text-gray-500 mt-1">{{ $t('mailbox.emailFixed') }}</p>
                </div>

                <div class="mb-4">
                  <label class="block text-sm font-medium text-gray-700 mb-2">
                    {{ $t('mailbox.password') }}
                  </label>
                  <div class="relative">
                    <input
                      :type="showPassword ? 'text' : 'password'"
                      v-model="newPassword"
                      placeholder="Min. 12 Zeichen"
                      class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required
                      minlength="12"
                    />
                    <button
                      type="button"
                      @click="showPassword = !showPassword"
                      class="absolute right-3 top-2.5 text-gray-600 hover:text-gray-900"
                    >
                      <svg v-if="showPassword" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                        <path fill-rule="evenodd"
                          d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                          clip-rule="evenodd" />
                      </svg>
                      <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd"
                          d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-14-14zM10 5c5.523 0 9.542 2.943 10.542 7-1 4.057-5.064 7-10.542 7a9.968 9.968 0 01-5.007-1.475l2.712-2.712A4 4 0 0110 5z"
                          clip-rule="evenodd" />
                      </svg>
                    </button>
                  </div>
                  <p class="text-xs text-gray-500 mt-1">{{ $t('mailbox.passwordInfo') }}</p>
                </div>

                <button
                  type="submit"
                  :disabled="creatingMailbox || !newPassword || newPassword.length < 12"
                  class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg font-semibold transition"
                >
                  <span v-if="creatingMailbox">{{ $t('common.creating') }}...</span>
                  <span v-else>{{ $t('mailbox.createMailbox') }}</span>
                </button>
              </form>
            </div>
          </div>
        </div>

        <!-- Mailbox Active State -->
        <div v-else class="space-y-6">
          <!-- Status Card -->
          <div class="bg-white rounded-lg shadow-lg p-6">
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-2xl font-bold text-gray-800">{{ $t('mailbox.mailboxStatus') }}</h2>
              <span :class="[
                'px-3 py-1 rounded-full text-sm font-semibold',
                mailboxStatus.active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
              ]">
                {{ mailboxStatus.active ? $t('mailbox.active') : $t('mailbox.inactive') }}
              </span>
            </div>

            <!-- Email Address -->
            <div class="mb-6">
              <label class="text-sm text-gray-600">{{ $t('mailbox.emailAddress') }}</label>
              <p class="text-xl font-semibold text-gray-900 break-all">{{ mailboxStatus.email }}</p>
            </div>

            <!-- Quota Bar -->
            <div class="mb-6">
              <div class="flex justify-between items-center mb-2">
                <label class="text-sm text-gray-600">{{ $t('mailbox.storage') }}</label>
                <span class="text-sm font-semibold text-gray-900">{{ quotaUsedMB }}MB / {{ mailboxStatus.quota_mb }}MB</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
                <div
                  :style="{ width: mailboxStatus.quota_percent + '%' }"
                  :class="[
                    'h-full transition-all',
                    mailboxStatus.quota_percent < 70 ? 'bg-green-500' :
                    mailboxStatus.quota_percent < 90 ? 'bg-yellow-500' :
                    'bg-red-500'
                  ]"
                ></div>
              </div>
              <p class="text-xs text-gray-500 mt-1">{{ mailboxStatus.quota_percent }}% {{ $t('mailbox.used') }}</p>
            </div>

            <!-- Created Date -->
            <div class="mb-4">
              <label class="text-sm text-gray-600">{{ $t('mailbox.createdAt') }}</label>
              <p class="text-gray-900">{{ formatDate(mailboxStatus.created_at) }}</p>
            </div>
          </div>

          <!-- Forwarding Rules Card -->
          <div class="bg-white rounded-lg shadow-lg p-6">
            <h3 class="text-xl font-bold text-gray-800 mb-4">{{ $t('mailbox.forwardingRules') }}</h3>

            <!-- Add Forwarding Form -->
            <form @submit.prevent="addForwarding" class="mb-6 p-4 bg-gray-50 rounded-lg">
              <div class="flex gap-3">
                <input
                  v-model="newForwarding"
                  type="email"
                  placeholder="Email address"
                  class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                  required
                />
                <button
                  type="submit"
                  :disabled="addingForwarding"
                  class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg font-semibold transition"
                >
                  {{ $t('common.add') }}
                </button>
              </div>
            </form>

            <!-- Forwarding List -->
            <div v-if="forwardingRules.length > 0" class="space-y-2">
              <div v-for="(rule, index) in forwardingRules" :key="index" class="flex items-center justify-between bg-gray-50 p-3 rounded-lg">
                <span class="text-gray-900">{{ rule }}</span>
                <button
                  @click="removeForwarding(rule)"
                  class="text-red-600 hover:text-red-800 text-sm font-semibold"
                >
                  {{ $t('common.remove') }}
                </button>
              </div>
            </div>
            <p v-else class="text-gray-600 text-center py-4">{{ $t('mailbox.noForwarding') }}</p>
          </div>

          <!-- Danger Zone -->
          <div class="bg-red-50 border border-red-200 rounded-lg shadow-lg p-6">
            <h3 class="text-xl font-bold text-red-900 mb-4">{{ $t('common.dangerZone') }}</h3>
            <p class="text-red-700 mb-4">{{ $t('mailbox.deleteWarning') }}</p>
            <button
              @click="confirmDelete = true"
              class="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg font-semibold transition"
            >
              {{ $t('mailbox.deleteMailbox') }}
            </button>
          </div>

          <!-- Delete Confirmation Modal -->
          <div v-if="confirmDelete" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div class="bg-white rounded-lg p-8 max-w-md mx-4">
              <h3 class="text-2xl font-bold text-red-900 mb-4">{{ $t('common.confirm') }}</h3>
              <p class="text-gray-700 mb-6">{{ $t('mailbox.deleteConfirm') }}</p>
              <div class="flex gap-4">
                <button
                  @click="confirmDelete = false"
                  class="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-900 px-4 py-2 rounded-lg font-semibold"
                >
                  {{ $t('common.cancel') }}
                </button>
                <button
                  @click="deleteMailbox"
                  :disabled="deletingMailbox"
                  class="flex-1 bg-red-600 hover:bg-red-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg font-semibold"
                >
                  {{ deletingMailbox ? $t('common.deleting') + '...' : $t('common.delete') }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuth } from '../stores/auth'
import api from '../lib/api'
import i18n from '../i18n'

const { state } = useAuth()
const t = i18n.global.t

// State
const loading = ref(true)
const error = ref(null)
const mailboxStatus = ref({
  enabled: false,
  username: '',
  email: '',
  quota_mb: 5120,
  quota_percent: 0,
  active: true,
  created_at: null,
})

const showPassword = ref(false)
const newPassword = ref('')
const creatingMailbox = ref(false)
const newForwarding = ref('')
const forwardingRules = ref([])
const addingForwarding = ref(false)
const confirmDelete = ref(false)
const deletingMailbox = ref(false)
const quotaUsedMB = ref(0)

// Methods
function extractUsername(email) {
  return email.split('@')[0]
}

function formatDate(dateString) {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('de-DE')
}

async function loadMailboxStatus() {
  loading.value = true
  error.value = null

  try {
    // Lade Mailbox Status
    const response = await api.get('/mailbox')
    mailboxStatus.value = response.data

    // Lade Quota
    try {
      const quotaResponse = await api.get('/mailbox/quota')
      quotaUsedMB.value = quotaResponse.data.quota_used_mb
    } catch (e) {
      console.warn('Could not load quota:', e)
    }

    // Lade Forwarding Rules
    if (mailboxStatus.value.enabled) {
      try {
        const fwdResponse = await api.get('/mailbox/forwarding')
        forwardingRules.value = fwdResponse.data.forwarding_rules || []
      } catch (e) {
        console.warn('Could not load forwarding rules:', e)
      }
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load mailbox status'
    console.error('Error loading mailbox:', err)
  } finally {
    loading.value = false
  }
}

async function createMailbox() {
  creatingMailbox.value = true
  error.value = null

  try {
    await api.post('/mailbox', {
      password: newPassword.value
    })

    newPassword.value = ''
    showPassword.value = false
    await loadMailboxStatus()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to create mailbox'
    console.error('Error creating mailbox:', err)
  } finally {
    creatingMailbox.value = false
  }
}

async function addForwarding() {
  addingForwarding.value = true
  error.value = null

  try {
    await api.post('/mailbox/forwarding', {
      destination: newForwarding.value,
      keep_local_copy: true
    })

    newForwarding.value = ''
    await loadMailboxStatus()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to add forwarding rule'
    console.error('Error adding forwarding:', err)
  } finally {
    addingForwarding.value = false
  }
}

async function removeForwarding(destination) {
  error.value = null

  try {
    await api.delete(`/mailbox/forwarding/${destination}`)
    await loadMailboxStatus()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to remove forwarding rule'
    console.error('Error removing forwarding:', err)
  }
}

async function deleteMailbox() {
  deletingMailbox.value = true
  error.value = null

  try {
    await api.delete('/mailbox')
    confirmDelete.value = false
    newPassword.value = ''
    await loadMailboxStatus()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to delete mailbox'
    console.error('Error deleting mailbox:', err)
  } finally {
    deletingMailbox.value = false
  }
}

// Lifecycle
onMounted(() => {
  loadMailboxStatus()
})
</script>

<style scoped>
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f4f6;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
