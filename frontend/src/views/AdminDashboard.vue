<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">{{ t('admin.title') }}</h1>
        <p class="mt-2 text-gray-600">{{ t('admin.description') }}</p>
      </div>

      <!-- Tabs -->
      <div class="mb-6">
        <div class="border-b border-gray-200">
          <div class="flex space-x-8">
            <button
              @click="activeTab = 'users'"
              :class="[
                'px-1 py-4 border-b-2 font-medium text-sm',
                activeTab === 'users'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              👥 {{ t('admin.users.title') }}
            </button>
            <button
              @click="activeTab = 'pages'"
              :class="[
                'px-1 py-4 border-b-2 font-medium text-sm',
                activeTab === 'pages'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              ]"
            >
              📄 {{ t('admin.pages.title') }}
            </button>
          </div>
        </div>
      </div>

      <!-- Tab Content -->
      <div>
        <!-- Users Tab -->
        <div v-if="activeTab === 'users'">
          <AdminUsers />
        </div>

        <!-- Pages Tab -->
        <div v-if="activeTab === 'pages'">
          <AdminPages />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import AdminUsers from './AdminUsers.vue'
import AdminPages from './AdminPages.vue'

const { t } = useI18n()

const activeTab = ref('users')
</script>
