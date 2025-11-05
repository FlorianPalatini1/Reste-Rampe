<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
    <!-- Header -->
    <header class="border-b border-slate-700 bg-slate-900/50 backdrop-blur-sm sticky top-0 z-40">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="text-2xl">🐮</div>
            <div>
              <h1 class="text-2xl font-bold text-white">Mailcow Monitoring</h1>
              <p class="text-sm text-slate-400">Real-time Performance Dashboard</p>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <div class="text-right">
              <p class="text-sm text-slate-400">Last Update</p>
              <p class="text-lg font-mono text-white">{{ lastUpdate }}</p>
            </div>
            <button
              @click="refreshData"
              :disabled="loading"
              class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition disabled:opacity-50"
            >
              <span v-if="!loading">🔄 Refresh</span>
              <span v-else>⏳ Loading...</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Error Alert -->
      <div v-if="error" class="mb-6 p-4 bg-red-900/20 border border-red-700 rounded-lg text-red-200">
        <p class="font-semibold">⚠️ Error</p>
        <p>{{ error }}</p>
      </div>

      <!-- Status Grid -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <!-- API Health -->
        <div class="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-slate-400">API Health</p>
              <p class="text-2xl font-bold text-white mt-2">
                {{ stats?.api_health?.status || 'N/A' }}
              </p>
              <p class="text-xs text-slate-500 mt-1">
                {{ stats?.api_health?.response_time_ms?.toFixed(0) || '0' }}ms
              </p>
            </div>
            <div class="text-3xl" :class="getStatusEmoji(stats?.api_health?.status)">
              {{ getStatusIcon(stats?.api_health?.status) }}
            </div>
          </div>
        </div>

        <!-- Total Mailboxes -->
        <div class="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-slate-400">Mailboxes</p>
              <p class="text-2xl font-bold text-white mt-2">
                {{ stats?.mailbox_summary?.total_mailboxes || 0 }}
              </p>
              <p class="text-xs text-slate-500 mt-1">Active</p>
            </div>
            <div class="text-3xl">📧</div>
          </div>
        </div>

        <!-- Average Usage -->
        <div class="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-slate-400">Avg Usage</p>
              <p class="text-2xl font-bold text-white mt-2">
                {{ stats?.mailbox_summary?.average_usage_percent?.toFixed(1) || '0' }}%
              </p>
              <p class="text-xs text-slate-500 mt-1">of Total Quota</p>
            </div>
            <div class="text-3xl">📊</div>
          </div>
        </div>

        <!-- Total Storage -->
        <div class="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-slate-400">Total Usage</p>
              <p class="text-2xl font-bold text-white mt-2">
                {{ formatBytes(stats?.mailbox_summary?.total_used_mb || 0) }}
              </p>
              <p class="text-xs text-slate-500 mt-1">
                / {{ formatBytes(stats?.mailbox_summary?.total_quota_mb || 0) }}
              </p>
            </div>
            <div class="text-3xl">💾</div>
          </div>
        </div>
      </div>

      <!-- Mailboxes Table -->
      <div class="bg-slate-800/50 border border-slate-700 rounded-lg p-6 mb-8">
        <h2 class="text-xl font-bold text-white mb-4">📬 Mailbox Usage</h2>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-slate-700">
                <th class="text-left py-3 px-4 text-slate-300 font-semibold">Mailbox</th>
                <th class="text-right py-3 px-4 text-slate-300 font-semibold">Used</th>
                <th class="text-right py-3 px-4 text-slate-300 font-semibold">Total</th>
                <th class="text-right py-3 px-4 text-slate-300 font-semibold">Usage %</th>
                <th class="text-center py-3 px-4 text-slate-300 font-semibold">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="mailbox in stats?.mailbox_summary?.mailboxes"
                :key="mailbox.mailbox"
                class="border-b border-slate-700/50 hover:bg-slate-700/20 transition"
              >
                <td class="py-3 px-4 text-white font-mono text-sm">
                  {{ mailbox.mailbox }}
                </td>
                <td class="py-3 px-4 text-right text-slate-300">
                  {{ formatBytes(mailbox.used_mb) }}
                </td>
                <td class="py-3 px-4 text-right text-slate-300">
                  {{ formatBytes(mailbox.total_mb) }}
                </td>
                <td class="py-3 px-4 text-right">
                  <div class="w-24 h-2 bg-slate-700 rounded-full overflow-hidden ml-auto">
                    <div
                      class="h-full rounded-full transition-all"
                      :class="getStatusColor(mailbox.status)"
                      :style="{ width: mailbox.usage_percent + '%' }"
                    ></div>
                  </div>
                  <p class="text-xs text-slate-400 mt-1">
                    {{ mailbox.usage_percent.toFixed(1) }}%
                  </p>
                </td>
                <td class="py-3 px-4 text-center">
                  <span
                    class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold"
                    :class="getStatusBadgeClass(mailbox.status)"
                  >
                    {{ mailbox.status }}
                  </span>
                </td>
              </tr>
              <tr v-if="!stats?.mailbox_summary?.mailboxes?.length">
                <td colspan="5" class="py-8 px-4 text-center text-slate-400">
                  No mailboxes available or API key not configured
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Forwarding Rules -->
      <div v-if="stats?.forwarding_rules?.length" class="bg-slate-800/50 border border-slate-700 rounded-lg p-6">
        <h2 class="text-xl font-bold text-white mb-4">🔀 Forwarding Rules</h2>
        <div class="space-y-3">
          <div
            v-for="(rule, idx) in stats.forwarding_rules"
            :key="idx"
            class="flex items-center justify-between p-3 bg-slate-700/30 rounded border border-slate-600/50"
          >
            <div class="flex-1">
              <p class="font-mono text-sm text-white">{{ rule.source }}</p>
              <p class="text-xs text-slate-400 mt-1">
                → {{ rule.destinations.join(', ') }}
              </p>
            </div>
            <div>
              <span
                v-if="rule.active"
                class="inline-flex items-center px-2 py-1 rounded text-xs font-semibold bg-green-900/30 text-green-400"
              >
                ✓ Active
              </span>
              <span v-else class="inline-flex items-center px-2 py-1 rounded text-xs font-semibold bg-red-900/30 text-red-400">
                ✗ Inactive
              </span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const stats = ref(null)
const loading = ref(false)
const error = ref(null)
const lastUpdate = ref('--:--:--')
let refreshInterval = null

const API_BASE = '/api/monitoring'

const getStatusIcon = (status) => {
  const icons = {
    HEALTHY: '✅',
    WARNING: '⚠️',
    CRITICAL: '❌',
  }
  return icons[status] || '❓'
}

const getStatusEmoji = (status) => {
  const emojis = {
    HEALTHY: 'text-green-400',
    WARNING: 'text-yellow-400',
    CRITICAL: 'text-red-400',
  }
  return emojis[status] || 'text-gray-400'
}

const getStatusColor = (status) => {
  const colors = {
    HEALTHY: 'bg-green-500',
    WARNING: 'bg-yellow-500',
    CRITICAL: 'bg-red-500',
  }
  return colors[status] || 'bg-gray-500'
}

const getStatusBadgeClass = (status) => {
  const classes = {
    HEALTHY: 'bg-green-900/30 text-green-400',
    WARNING: 'bg-yellow-900/30 text-yellow-400',
    CRITICAL: 'bg-red-900/30 text-red-400',
  }
  return classes[status] || 'bg-gray-900/30 text-gray-400'
}

const formatBytes = (mb) => {
  if (mb >= 1024) {
    return (mb / 1024).toFixed(1) + ' GB'
  }
  return mb.toFixed(1) + ' MB'
}

const updateTime = () => {
  const now = new Date()
  lastUpdate.value = now.toLocaleTimeString()
}

const refreshData = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await fetch(`${API_BASE}/api/stats`)
    if (!response.ok) {
      throw new Error('Failed to fetch monitoring data')
    }
    
    stats.value = await response.json()
    updateTime()
  } catch (err) {
    error.value = err.message || 'Failed to load monitoring data'
    console.error('Error fetching stats:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  refreshData()
  updateTime()
  
  // Refresh every 30 seconds
  refreshInterval = setInterval(() => {
    refreshData()
  }, 30000)
  
  // Update time every second
  setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style scoped>
/* Add any additional styling here */
</style>
