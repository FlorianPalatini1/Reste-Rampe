<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900">Admin - Seiten verwalten</h1>
        <p class="mt-2 text-gray-600">Bearbeite alle statischen Seiten</p>
      </div>

      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">Lade Seiten...</p>
      </div>

      <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
        <p class="text-red-700">{{ error }}</p>
      </div>

      <!-- Page Type Selector -->
      <div v-if="!loading" class="mb-6 bg-white shadow rounded-lg p-6">
        <label class="block text-sm font-medium text-gray-700 mb-3">Seite auswählen</label>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
          <button
            v-for="pageType in pageTypes"
            :key="pageType.key"
            @click="loadPageByType(pageType.key)"
            :class="[
              'px-4 py-2 rounded-lg text-sm font-medium transition',
              selectedPageType === pageType.key
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]"
          >
            {{ pageType.label }}
          </button>
        </div>
      </div>

      <!-- Page Editor -->
      <template v-if="!loading && currentPage">
        <div class="bg-white shadow rounded-lg p-6">
          <form @submit.prevent="savePage" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Titel</label>
              <input v-model="currentPage.title" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Sprache</label>
              <select v-model="selectedLanguage" @change="switchLanguage" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                <option value="de">🇩🇪 Deutsch</option>
                <option value="en">🇬🇧 English</option>
                <option value="fr">🇫🇷 Français</option>
                <option value="ja">🇯🇵 日本語</option>
                <option value="tr">🇹🇷 Türkçe</option>
                <option value="fa">🇮🇷 فارسی</option>
                <option value="nds">🇩🇪 Plattdüütsch</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Inhalt (Markdown)</label>
              <div class="mb-2 flex gap-2 border-b border-gray-200 pb-2">
                <button type="button" @click="insertMarkdown('heading')" class="px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded" title="Überschrift">H</button>
                <button type="button" @click="insertMarkdown('bold')" class="px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded font-bold" title="Fett">B</button>
                <button type="button" @click="insertMarkdown('italic')" class="px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded italic" title="Kursiv">I</button>
                <button type="button" @click="insertMarkdown('list')" class="px-2 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded" title="Liste">• List</button>
              </div>
              <textarea ref="contentTextarea" v-model="currentPage.content" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm" rows="15"></textarea>
              <p class="mt-1 text-xs text-gray-500">Markdown wird unterstützt</p>
            </div>

            <!-- Preview -->
            <div v-if="currentPage.content" class="border-t pt-4">
              <h3 class="text-sm font-medium text-gray-700 mb-2">Vorschau</h3>
              <div class="prose prose-sm max-w-none bg-gray-50 rounded p-4" v-html="renderedContent" />
            </div>

            <!-- Action Buttons -->
            <div class="flex justify-end gap-2 pt-4 border-t border-gray-200">
              <button type="button" @click="resetPage" class="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">Abbrechen</button>
              <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700" :disabled="saving">{{ saving ? 'Speichert...' : 'Speichern' }}</button>
            </div>
          </form>
        </div>
      </template>

      <!-- No Page Found -->
      <div v-if="!loading && !currentPage" class="text-center py-12 bg-white rounded-lg">
        <p class="text-gray-500">Keine Seiten gefunden</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { marked } from 'marked'
import api from '../lib/api'

const pageTypes = [
  { key: 'privacy', label: '🔒 Datenschutz' },
  { key: 'imprint', label: '📋 Impressum' },
  { key: 'terms', label: '📜 Nutzungsbedingungen' },
  { key: 'agb', label: '⚖️ AGB' }
]

const currentPage = ref(null)
const originalContent = ref(null)
const loading = ref(true)
const saving = ref(false)
const error = ref('')
const contentTextarea = ref(null)
const selectedLanguage = ref('de')
const selectedPageType = ref('privacy')
const allPages = ref([])

const loadPages = async () => {
  loading.value = true
  error.value = ''
  try {
    console.log('🔄 Loading all pages from /api/pages')
    const response = await api.get('/pages')
    console.log('✅ Pages loaded:', response.data)
    allPages.value = response.data || []
    
    // Load first page type
    loadPageByType(selectedPageType.value)
  } catch (err) {
    console.error('❌ Error loading pages:', err)
    error.value = `Fehler beim Laden der Seiten: ${err.response?.data?.detail || err.message}`
    loading.value = false
  }
}

const loadPageByType = (pageKey) => {
  selectedPageType.value = pageKey
  const page = allPages.value.find(p => p.page_key === pageKey && p.language === 'de')
  
  if (page) {
    currentPage.value = { ...page }
    originalContent.value = page.content
    selectedLanguage.value = 'de'
  } else {
    currentPage.value = null
    error.value = `Seite "${pageKey}" nicht gefunden`
  }
  loading.value = false
}

const switchLanguage = async (lang) => {
  selectedLanguage.value = lang
  loading.value = true
  try {
    const page = allPages.value.find(p => p.page_key === selectedPageType.value && p.language === lang)

    if (page) {
      currentPage.value = { ...page }
      originalContent.value = page.content
    } else {
      error.value = `Seite in der Sprache "${lang}" nicht gefunden`
    }
  } catch (err) {
    console.error('❌ Error loading page:', err)
  } finally {
    loading.value = false
  }
}

const savePage = async () => {
  if (!currentPage.value) return

  saving.value = true
  try {
    console.log('💾 Saving page:', currentPage.value.id)
    const response = await api.put(`/pages/${currentPage.value.id}`, {
      title: currentPage.value.title,
      content: currentPage.value.content,
      language: currentPage.value.language
    })
    console.log('✅ Page saved:', response.data)

    currentPage.value = response.data
    originalContent.value = response.data.content
    alert('Seite gespeichert!')
  } catch (err) {
    console.error('❌ Error saving page:', err)
    alert(err.response?.data?.detail || 'Fehler beim Speichern')
  } finally {
    saving.value = false
  }
}

const resetPage = () => {
  if (currentPage.value && originalContent.value) {
    currentPage.value.content = originalContent.value
  }
}

const insertMarkdown = (type) => {
  const textarea = contentTextarea.value
  if (!textarea) return

  const start = textarea.selectionStart
  const end = textarea.selectionEnd
  const selected = currentPage.value.content.substring(start, end)

  let insertion = ''
  if (type === 'heading') {
    insertion = `\n## ${selected || 'Überschrift'}\n`
  } else if (type === 'bold') {
    insertion = `**${selected || 'fett'}**`
  } else if (type === 'italic') {
    insertion = `*${selected || 'kursiv'}*`
  } else if (type === 'list') {
    insertion = `\n- Punkt 1\n- Punkt 2\n- Punkt 3\n`
  }

  const newContent = currentPage.value.content.substring(0, start) + insertion + currentPage.value.content.substring(end)
  currentPage.value.content = newContent

  setTimeout(() => {
    textarea.selectionStart = textarea.selectionEnd = start + insertion.length
    textarea.focus()
  }, 0)
}

const renderedContent = computed(() => {
  if (!currentPage.value?.content) return ''
  try {
    return marked(currentPage.value.content)
  } catch (e) {
    console.error('Markdown render error:', e)
    return '<pre>' + currentPage.value.content + '</pre>'
  }
})

onMounted(() => {
  loadPages()
})
</script>

<style scoped>
textarea {
  resize: vertical;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}
</style>
