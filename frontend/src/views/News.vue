<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-8 flex justify-between items-center">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">{{ t('news.title') }}</h1>
          <p class="mt-2 text-gray-600">{{ t('news.subtitle') }}</p>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        <p class="mt-4 text-gray-600">{{ t('common.loading') }}</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
        <p class="text-red-700">{{ error }}</p>
      </div>

      <!-- News Grid -->
      <div v-if="!loading && articles.length > 0" class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <article
          v-for="article in articles"
          :key="article.id"
          class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow overflow-hidden cursor-pointer"
          @click="viewArticle(article)"
        >
          <div class="p-6">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-semibold text-primary-600 uppercase tracking-wider">
                {{ t('news.published') }}
              </span>
              <time class="text-xs text-gray-500">{{ formatDate(article.published_at) }}</time>
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-2 line-clamp-2">{{ article.title }}</h3>
            <p v-if="article.excerpt" class="text-gray-600 text-sm line-clamp-2 mb-4">
              {{ article.excerpt }}
            </p>
            <div class="text-primary-600 hover:text-primary-700 font-semibold text-sm">
              {{ t('news.readMore') }} →
            </div>
          </div>
        </article>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && articles.length === 0" class="text-center py-12">
        <p class="text-gray-500">{{ t('news.noArticles') }}</p>
      </div>

      <!-- Pagination -->
      <div v-if="!loading && articles.length > 0" class="mt-8 flex justify-center gap-4">
        <button
          v-if="skip > 0"
          @click="skip -= limit"
          class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
        >
          {{ t('common.previous') }}
        </button>
        <span class="px-4 py-2 text-gray-700">
          {{ skip / limit + 1 }} / {{ Math.ceil(total / limit) }}
        </span>
        <button
          v-if="skip + limit < total"
          @click="skip += limit"
          class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
        >
          {{ t('common.next') }}
        </button>
      </div>

      <!-- Article Detail Modal -->
      <div v-if="selectedArticle" class="fixed z-10 inset-0 overflow-y-auto">
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
          <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <div class="flex justify-between items-start mb-4">
                <div>
                  <h3 class="text-2xl font-bold text-gray-900">{{ selectedArticle.title }}</h3>
                  <p class="text-sm text-gray-500 mt-1">{{ formatDate(selectedArticle.published_at) }}</p>
                  <p v-if="selectedArticle.category" class="text-sm text-primary-600 font-semibold mt-1">{{ selectedArticle.category }}</p>
                </div>
                <button @click="selectedArticle = null" class="text-gray-400 hover:text-gray-500">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div class="prose prose-sm max-w-none" v-html="getArticleHtml(selectedArticle.content)"></div>

              <div v-if="selectedArticle.source" class="mt-6 pt-4 border-t border-gray-200 text-sm text-gray-500">
                <strong>{{ t('news.source') || 'Source' }}:</strong> {{ selectedArticle.source }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { newsAPI } from '../services/api'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const { t, locale } = useI18n()
const router = useRouter()

const articles = ref([])
const loading = ref(true)
const error = ref('')
const skip = ref(0)
const limit = ref(6)
const total = ref(0)
const selectedArticle = ref(null)

const loadArticles = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await newsAPI.getAll(skip.value, limit.value)
    console.log('News API Response:', response)
    // Response könnte direkt ein Array sein oder in response.data sein
    articles.value = Array.isArray(response) ? response : response.data
    total.value = articles.value.length + skip.value
  } catch (err) {
    console.error('Error loading articles:', err)
    error.value = err?.response?.data?.detail || t('news.loadError') || 'Error loading articles'
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString(locale.value || 'de-DE', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const viewArticle = (article) => {
  selectedArticle.value = article
}

const getArticleHtml = (content) => {
  if (!content) return ''
  try {
    const html = marked.parse(content)
    return DOMPurify.sanitize(html)
  } catch {
    return DOMPurify.sanitize(content)
  }
}

watch(() => locale.value, () => {
  skip.value = 0
  loadArticles()
})

watch(() => skip.value, () => {
  loadArticles()
})

onMounted(() => {
  loadArticles()
})
</script>
