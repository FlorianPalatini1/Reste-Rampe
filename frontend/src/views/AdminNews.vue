<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-8 flex justify-between items-center">
        <div>
          <h1 class="text-3xl font-bold text-gray-900">{{ t('admin.news.title') }}</h1>
          <p class="mt-2 text-gray-600">{{ t('admin.news.subtitle') }}</p>
        </div>
        <button
          @click="showCreateModal = true"
          class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700"
        >
          {{ t('admin.news.createBtn') }}
        </button>
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

      <!-- Articles Table -->
      <div v-if="!loading && articles.length > 0" class="bg-white shadow rounded-lg overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ t('admin.news.title') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ t('admin.news.status') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ t('admin.news.created') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ t('common.actions') }}
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="article in articles" :key="article.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">{{ article.title }}</div>
                <div class="text-xs text-gray-500">/{{ article.slug }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="[
                    'px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full',
                    article.is_published
                      ? 'bg-green-100 text-green-800'
                      : 'bg-yellow-100 text-yellow-800'
                  ]"
                >
                  {{ article.is_published ? t('admin.news.published') : t('admin.news.draft') }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                {{ formatDate(article.created_at) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                <button
                  @click="editArticle(article)"
                  class="text-blue-600 hover:text-blue-900"
                >
                  {{ t('common.edit') }}
                </button>
                <button
                  v-if="!article.is_published"
                  @click="publishArticle(article)"
                  class="text-green-600 hover:text-green-900"
                >
                  {{ t('admin.news.publishBtn') }}
                </button>
                <button
                  v-if="article.is_published"
                  @click="unpublishArticle(article)"
                  class="text-yellow-600 hover:text-yellow-900"
                >
                  {{ t('admin.news.unpublishBtn') }}
                </button>
                <button
                  @click="deleteArticle(article)"
                  class="text-red-600 hover:text-red-900"
                >
                  {{ t('common.delete') }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && articles.length === 0" class="text-center py-12 bg-white rounded-lg">
        <p class="text-gray-500 mb-4">{{ t('admin.news.noArticles') }}</p>
        <button
          @click="showCreateModal = true"
          class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700"
        >
          {{ t('admin.news.createFirst') }}
        </button>
      </div>

      <!-- Create/Edit Modal -->
      <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full p-6">
          <h2 class="text-2xl font-bold mb-4">
            {{ editingArticle ? t('admin.news.edit') : t('admin.news.create') }}
          </h2>

          <form @submit.prevent="saveArticle" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                {{ t('admin.news.titleLabel') }}
              </label>
              <input
                v-model="form.title"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                {{ t('admin.news.excerptLabel') }}
              </label>
              <textarea
                v-model="form.excerpt"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                rows="2"
              ></textarea>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                {{ t('admin.news.contentLabel') }}
              </label>
              <textarea
                v-model="form.content"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 font-mono text-sm"
                rows="10"
                required
              ></textarea>
              <p class="mt-1 text-xs text-gray-500">{{ t('admin.news.htmlSupported') }}</p>
            </div>

            <div class="flex justify-end gap-2 pt-4">
              <button
                type="button"
                @click="showCreateModal = false"
                class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                {{ t('common.cancel') }}
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
              >
                {{ editingArticle ? t('common.save') : t('admin.news.createBtn') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import axios from 'axios'

const { t } = useI18n()

const API_URL = import.meta.env.VITE_API_URL || '/api'

const articles = ref([])
const loading = ref(true)
const error = ref('')
const showCreateModal = ref(false)
const editingArticle = ref(null)
const form = ref({
  title: '',
  excerpt: '',
  content: ''
})

const loadArticles = async () => {
  loading.value = true
  error.value = ''
  try {
    const token = localStorage.getItem('access_token')
    const response = await axios.get(`${API_URL}/api/news/admin/all`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    articles.value = response.data
  } catch (err) {
    console.error('Error loading articles:', err)
    error.value = t('admin.news.loadError')
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

const editArticle = (article) => {
  editingArticle.value = article
  form.value = {
    title: article.title,
    excerpt: article.excerpt || '',
    content: article.content
  }
  showCreateModal.value = true
}

const saveArticle = async () => {
  try {
    const token = localStorage.getItem('access_token')
    
    if (editingArticle.value) {
      // Update existing
      await axios.patch(`${API_URL}/api/news/admin/${editingArticle.value.id}`, form.value, {
        headers: { Authorization: `Bearer ${token}` }
      })
    } else {
      // Create new
      await axios.post(`${API_URL}/api/news/admin`, form.value, {
        headers: { Authorization: `Bearer ${token}` }
      })
    }
    
    showCreateModal.value = false
    editingArticle.value = null
    form.value = { title: '', excerpt: '', content: '' }
    await loadArticles()
  } catch (err) {
    console.error('Error saving article:', err)
    alert(t('admin.news.saveError'))
  }
}

const publishArticle = async (article) => {
  try {
    const token = localStorage.getItem('access_token')
    await axios.patch(`${API_URL}/api/news/admin/${article.id}/publish`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    })
    await loadArticles()
  } catch (err) {
    console.error('Error publishing:', err)
    alert(t('admin.news.publishError'))
  }
}

const unpublishArticle = async (article) => {
  try {
    const token = localStorage.getItem('access_token')
    await axios.patch(`${API_URL}/api/news/admin/${article.id}/unpublish`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    })
    await loadArticles()
  } catch (err) {
    console.error('Error unpublishing:', err)
    alert(t('admin.news.unpublishError'))
  }
}

const deleteArticle = async (article) => {
  if (!confirm(t('admin.news.confirmDelete'))) return
  
  try {
    const token = localStorage.getItem('access_token')
    await axios.delete(`${API_URL}/api/news/admin/${article.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    await loadArticles()
  } catch (err) {
    console.error('Error deleting:', err)
    alert(t('admin.news.deleteError'))
  }
}

onMounted(() => {
  loadArticles()
})
</script>
