<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
      <div class="bg-white shadow overflow-hidden rounded-lg">
        <!-- Header -->
        <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
          <h1 class="text-3xl font-bold text-gray-900">{{ pageContent.title }}</h1>
          <p v-if="pageContent.updated_at" class="mt-1 text-sm text-gray-500">
            {{ t('privacy.lastUpdated') }}: {{ formatDate(pageContent.updated_at) }}
          </p>
        </div>

        <!-- Content -->
        <div class="px-4 py-5 sm:px-6">
          <div v-if="loading" class="text-center py-12">
            <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            <p class="mt-4 text-gray-600">{{ t('common.loading') }}</p>
          </div>

          <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
            <p class="text-red-700">{{ error }}</p>
          </div>

          <div v-if="!loading && !error" class="prose prose-lg max-w-none">
            <div v-html="pageContent.content"></div>
          </div>
        </div>

        <!-- Back Button -->
        <div class="px-4 py-4 sm:px-6 border-t border-gray-200 flex justify-between">
          <router-link to="/dashboard" class="text-primary-600 hover:text-primary-800 font-semibold">
            ← {{ t('common.backOverview') }}
          </router-link>
          <router-link
            v-if="isAdmin"
            to="/admin/pages"
            class="text-primary-600 hover:text-primary-800 font-semibold"
          >
            {{ t('privacy.editPage') }} →
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const { t, locale } = useI18n()
const route = useRoute()

// Use relative URL for local dev (proxied by Vite) or absolute for production
const API_URL = '/api'

// Map route name to page_key
const pageKeyMap = {
  'privacy': 'privacy',
  'imprint': 'imprint',
  'terms': 'terms',
  'agb': 'agb'
}

const pageKey = computed(() => pageKeyMap[route.name] || 'privacy')

const pageContent = ref({
  title: t('privacy.title'),
  content: t('common.loading'),
  updated_at: null
})
const loading = ref(true)
const error = ref('')
const isAdmin = ref(false)

const loadPageContent = async () => {
  loading.value = true
  error.value = ''
  try {
    // Immer die AKTUELLE Sprache vom i18n benutzen, nicht die gespeicherte
    const currentLang = locale.value || 'de'
    const url = `${API_URL}/pages/public/${pageKey.value}?language=${currentLang}`
    console.log('🔄 Loading page:', pageKey.value, 'with language:', currentLang, 'URL:', url)
    const response = await axios.get(url)
    console.log('✅ Page loaded:', response.data.language, '-', response.data.title)
    
    // Convert markdown to HTML and sanitize it
    const htmlContent = marked(response.data.content)
    const sanitizedContent = DOMPurify.sanitize(htmlContent)
    
    pageContent.value = {
      ...response.data,
      content: sanitizedContent
    }
    console.log('✅ pageContent.value updated:', pageContent.value)
  } catch (err) {
    console.error('❌ Error loading page:', err)
    error.value = t('common.error')
    pageContent.value.content = t('common.error')
  } finally {
    loading.value = false
    console.log('✅ Loading complete. Loading:', loading.value)
  }
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('de-DE', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const checkAdmin = async () => {
  try {
    const token = localStorage.getItem('access_token')
    if (token) {
      const response = await axios.get(`${API_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      isAdmin.value = response.data.is_admin
    }
  } catch (err) {
    isAdmin.value = false
  }
}

onMounted(() => {
  loadPageContent()
  checkAdmin()
})

// Reload page content when language changes or route changes
watch([locale, () => route.name], () => {
  loadPageContent()
})
</script>

<style scoped>
.prose {
  color: #374151;
  line-height: 1.75;
}

.prose :deep(h2) {
  font-size: 1.875rem;
  font-weight: 700;
  margin-top: 2rem;
  margin-bottom: 1rem;
  color: #111827;
}

.prose :deep(h3) {
  font-size: 1.5rem;
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  color: #1f2937;
}

.prose :deep(p) {
  margin-bottom: 1rem;
}

.prose :deep(ul),
.prose :deep(ol) {
  margin-left: 1.5rem;
  margin-bottom: 1rem;
}

.prose :deep(li) {
  margin-bottom: 0.5rem;
}
</style>
