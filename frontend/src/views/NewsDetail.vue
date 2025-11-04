<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        <p class="mt-4 text-gray-600">{{ t('common.loading') }}</p>
      </div>

      <!-- Error State -->
      <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
        <p class="text-red-700">{{ error }}</p>
      </div>

      <!-- Article Content -->
      <article v-if="!loading && article" class="bg-white rounded-lg shadow-lg p-8">
        <!-- Header -->
        <header class="mb-8 pb-8 border-b border-gray-200">
          <div class="flex items-center gap-4 mb-4 text-sm text-gray-600">
            <time>{{ formatDate(article.published_at) }}</time>
            <span>{{ t('news.by') }}</span>
            <span class="font-semibold">{{ article.author_id }}</span>
          </div>
          <h1 class="text-4xl font-bold text-gray-900 mb-2">{{ article.title }}</h1>
          <p v-if="article.excerpt" class="text-xl text-gray-600">{{ article.excerpt }}</p>
        </header>

        <!-- Content -->
        <div class="prose prose-lg max-w-none mb-8">
          <div v-html="article.content"></div>
        </div>

        <!-- Back Button -->
        <div class="mt-8 pt-8 border-t border-gray-200">
          <router-link to="/news" class="text-primary-600 hover:text-primary-800 font-semibold">
            ← {{ t('news.backToNews') }}
          </router-link>
        </div>
      </article>

      <!-- Not Found State -->
      <div v-if="!loading && !article" class="text-center py-12">
        <p class="text-gray-500 mb-4">{{ t('news.articleNotFound') }}</p>
        <router-link to="/news" class="text-primary-600 hover:text-primary-800 font-semibold">
          {{ t('news.backToNews') }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import axios from 'axios'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()

const API_URL = import.meta.env.VITE_API_URL || '/api'

const article = ref(null)
const loading = ref(true)
const error = ref('')

const loadArticle = async () => {
  loading.value = true
  error.value = ''
  try {
    const response = await axios.get(
      `${API_URL}/api/news/public/${route.params.slug}`
    )
    article.value = response.data
  } catch (err) {
    console.error('Error loading article:', err)
    error.value = t('news.loadError')
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('de-DE', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  loadArticle()
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

.prose :deep(strong) {
  font-weight: 600;
  color: #1f2937;
}

.prose :deep(em) {
  font-style: italic;
  color: #4b5563;
}

.prose :deep(a) {
  color: #2563eb;
  text-decoration: underline;
}

.prose :deep(a:hover) {
  color: #1d4ed8;
}
</style>
