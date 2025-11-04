<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">{{ t('admin.users.title') }}</h1>
        <p class="mt-2 text-gray-600">{{ t('admin.users.description') }}</p>
      </div>

      <!-- Debug Info -->
      <div class="mb-4 p-2 bg-blue-100 text-blue-800 rounded text-sm">
        Loading: {{ loading }} | Users: {{ users.length }} | Error: {{ error ? 'Yes' : 'No' }}
      </div>

      <!-- Loading & Error States -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        <p class="mt-4 text-gray-600">{{ t('common.loading') }}</p>
      </div>

      <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
        <p class="text-red-700">{{ error }}</p>
      </div>

      <!-- Users Table -->
      <div v-if="!loading && users.length > 0" class="bg-white shadow rounded-lg overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ t('admin.users.email') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ t('admin.users.username') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ t('admin.users.joined') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ t('admin.users.lastLogin') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ t('admin.users.status') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ t('admin.users.role') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ t('common.actions') }}
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ user.email }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">{{ user.username }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                {{ formatDate(user.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                {{ user.last_login ? formatDate(user.last_login) : t('admin.users.never') }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                  {{ t('admin.users.active') }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="[
                    'px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full',
                    user.is_admin
                      ? 'bg-blue-100 text-blue-800'
                      : 'bg-gray-100 text-gray-800'
                  ]"
                >
                  {{ user.is_admin ? t('admin.users.admin') : t('admin.users.user') }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                <button
                  v-if="!user.is_admin"
                  @click="makeAdmin(user)"
                  class="text-blue-600 hover:text-blue-900"
                  :title="t('admin.users.makeAdmin')"
                >
                  {{ t('admin.users.promoteBtn') }}
                </button>
                <button
                  v-if="user.is_admin && user.id !== currentUserId"
                  @click="removeAdmin(user)"
                  class="text-yellow-600 hover:text-yellow-900"
                  :title="t('admin.users.removeAdmin')"
                >
                  {{ t('admin.users.demoteBtn') }}
                </button>
                <button
                  v-if="user.id !== currentUserId"
                  @click="deleteUser(user)"
                  class="text-red-600 hover:text-red-900"
                  :title="t('admin.users.delete')"
                >
                  {{ t('admin.users.deleteBtn') }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && users.length === 0" class="text-center py-12">
        <p class="text-gray-500">{{ t('admin.users.noUsers') }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import api from '../lib/api'
import { useAuth } from '../stores/auth'

const { t } = useI18n()

const { getToken } = useAuth()
const getAuthToken = () => getToken() || localStorage.getItem('token') || localStorage.getItem('access_token')

const users = ref([])
const loading = ref(true)
const error = ref('')
const currentUserId = ref(null)

const loadUsers = async () => {
  loading.value = true
  error.value = ''
  try {
    console.log('🔄 Loading current user from /auth/me')
    const meResponse = await api.get('/auth/me')
    console.log('✅ Current user:', meResponse.data)
    currentUserId.value = meResponse.data.id
    
    console.log('🔄 Loading all users from /users/')
    const response = await api.get('/users/')
    console.log('✅ Users loaded:', response.data)
    console.log('📊 Total users:', response.data.length)
    users.value = response.data
    console.log('✅ users.value updated:', users.value)
  } catch (err) {
    console.error('❌ Error loading users:', err)
    console.error('Error response:', err.response?.status, err.response?.data)
    console.error('Error message:', err.message)
    error.value = `${t('admin.users.loadError')}: ${err.response?.data?.detail || err.message}`
  } finally {
    loading.value = false
    console.log('⏹️ Loading finished. Users count:', users.value.length)
  }
}

const formatDate = (dateString) => {
  if (!dateString) return t('admin.users.never')
  return new Date(dateString).toLocaleDateString('de-DE', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const makeAdmin = async (user) => {
  if (!confirm(t('admin.users.confirmPromote'))) return
  
  try {
    const response = await api.put(`/users/${user.id}/admin`, {})
    // Update local user
    const index = users.value.findIndex(u => u.id === user.id)
    if (index !== -1) users.value[index] = response.data
  } catch (err) {
    console.error('Error promoting user:', err)
    alert(err.response?.data?.detail || t('common.error'))
  }
}

const removeAdmin = async (user) => {
  if (!confirm(t('admin.users.confirmDemote'))) return
  
  try {
    const response = await api.delete(`/users/${user.id}/admin`)
    const index = users.value.findIndex(u => u.id === user.id)
    if (index !== -1) users.value[index] = response.data
  } catch (err) {
    console.error('Error demoting user:', err)
    alert(err.response?.data?.detail || t('common.error'))
  }
}

const activateUser = async (user) => {
  // Placeholder - activate/deactivate not yet implemented in backend
}

const deactivateUser = async (user) => {
  // Placeholder - activate/deactivate not yet implemented in backend
}

const deleteUser = async (user) => {
  if (!confirm(t('admin.users.confirmDelete'))) return

  try {
    await api.delete(`/users/${user.id}`)
    // remove locally
    users.value = users.value.filter(u => u.id !== user.id)
  } catch (err) {
    console.error('Error deleting user:', err)
    alert(err.response?.data?.detail || t('common.error'))
  }
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
