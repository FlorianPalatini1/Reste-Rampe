<template>
  <div class="px-4 py-6 sm:px-0">
    <h2 class="text-3xl font-bold text-gray-900 mb-6">{{ t('dashboard.title') }}</h2>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="text-4xl icon-sepia icon-grain">🥬</div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">{{ t('dashboard.allIngredients') }}</dt>
                <dd class="text-3xl font-semibold text-gray-900">{{ stats.totalIngredients }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="text-4xl icon-sepia icon-grain">❄️</div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">{{ t('ingredients.fridge') }}</dt>
                <dd class="text-3xl font-semibold text-gray-900">{{ stats.fridgeItems }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="text-4xl icon-sepia icon-grain">🗄️</div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">{{ t('ingredients.pantry') }}</dt>
                <dd class="text-3xl font-semibold text-gray-900">{{ stats.pantryItems }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="text-4xl icon-sepia icon-grain">⚠️</div>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">{{ t('dashboard.expiringItems') }}</dt>
                <dd class="text-3xl font-semibold text-red-600">{{ stats.expiringSoon }}</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Expiring Items Alert -->
    <div v-if="expiringItems.length > 0" class="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
      <div class="flex">
          <div class="flex-shrink-0 icon-sepia">
          <svg class="h-5 w-5 icon-force-current" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">{{ t('dashboard.expiringItems') }}</h3>
          <div class="mt-2 text-sm text-red-700">
            <ul class="list-disc list-inside space-y-1">
              <li v-for="item in expiringItems" :key="item.id">
                {{ item.name }} - {{ t('ingredients.expiryDate') }}: {{ formatDate(item.expiry_date) }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="bg-white shadow rounded-lg p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">{{ t('common.loading') === 'Loading...' ? 'Quick Actions' : 'Quick Actions' }}</h3>
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-4">
        <router-link
          to="/ingredients"
          class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
        >
          <span class="text-black">{{ t('ingredients.add') }}</span>
        </router-link>
        <router-link
          to="/shopping"
          class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
        >
          <span class="text-black">{{ t('shopping.create') }}</span>
        </router-link>
        <router-link
          to="/recipes"
          class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700"
        >
          <span class="text-black">{{ t('recipes.findRecipes') }}</span>
        </router-link>
        <button
          @click="showAiModal = true"
          class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-emerald-600 hover:bg-emerald-700"
        >
          <span class="icon-sepia mr-2">🤖</span><span class="text-black">{{ t('recipes.generate') }}</span>
        </button>
      </div>
    </div>

    <!-- AI Recipe Modal -->
    <div v-if="showAiModal" class="fixed z-10 inset-0 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <h3 class="text-lg font-medium text-gray-900 mb-4">{{ t('recipes.generate') }}</h3>
            <div class="space-y-4">
              <input v-model="dietary" type="text" :placeholder="t('recipes.dietary')"
                     class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500">
              <div v-if="aiRecipe" class="prose prose-sm max-w-none border rounded-md p-3">
                <div v-html="aiHtml"></div>
              </div>
              <div v-if="aiRecipe" class="mt-3 flex items-center space-x-2">
                <input v-model="aiTitle" type="text" :placeholder="t('recipes.title') || 'Recipe title (optional)'"
                       class="flex-1 border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500">
                <button @click="saveAIRecipe"
                        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
                  {{ t('common.save') }}
                </button>
              </div>
            </div>
            <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
              <button type="button" @click="generateAIRecipe"
                class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-emerald-600 text-base font-medium text-white hover:bg-emerald-700 focus:outline-none sm:col-start-2 sm:text-sm">
                {{ t('recipes.generate') }}
              </button>
              <button type="button" @click="closeAiModal"
                class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none sm:mt-0 sm:col-start-1 sm:text-sm">
                {{ t('common.close') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { ingredientsAPI } from '../services/api.js'
import { recipesAPI } from '../services/api.js'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const { t } = useI18n()

const stats = ref({
  totalIngredients: 0,
  fridgeItems: 0,
  pantryItems: 0,
  expiringSoon: 0
})

const expiringItems = ref([])
const showAiModal = ref(false)
const aiRecipe = ref('')
const aiTitle = ref('')
const dietary = ref('')

const aiHtml = computed(() => {
  try {
    const html = marked.parse(aiRecipe.value || '')
    return DOMPurify.sanitize(html)
  } catch {
    return DOMPurify.sanitize(aiRecipe.value || '')
  }
})

const loadDashboard = async () => {
  try {
    // Load all ingredients once
    const response = await ingredientsAPI.getAll()
    const allItems = response.data || []

    // Calculate stats based on location and expiry
    const fridgeItems = allItems.filter(item => item.location === 'Fridge')
    const pantryItems = allItems.filter(item => item.location === 'Pantry')
    
    // Check for expiring items (within 7 days)
    const today = new Date()
    const expiring = allItems.filter(item => {
      if (!item.expiry_date) return false
      const expiry = new Date(item.expiry_date)
      const diffDays = Math.ceil((expiry - today) / (1000 * 60 * 60 * 24))
      return diffDays <= 7 && diffDays >= 0
    })

    stats.value = {
      totalIngredients: allItems.length,
      fridgeItems: fridgeItems.length,
      pantryItems: pantryItems.length,
      expiringSoon: expiring.length
    }

    expiringItems.value = expiring
  } catch (error) {
    console.error('Error loading dashboard:', error)
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

onMounted(() => {
  loadDashboard()
})

const generateAIRecipe = async () => {
  try {
    const { data } = await recipesAPI.generateFromIngredients(dietary.value || null)
    aiRecipe.value = data.text || 'No recipe generated.'
  } catch (e) {
    console.error('AI generation failed', e)
    aiRecipe.value = e?.response?.data?.detail || 'AI generation failed.'
  }
}

const closeAiModal = () => {
  showAiModal.value = false
  // Keep content so user can re-open; comment below to clear if desired
  // aiRecipe.value = ''
}

const saveAIRecipe = async () => {
  try {
    const { data } = await recipesAPI.saveFromAI(aiRecipe.value, aiTitle.value || null)
    aiTitle.value = ''
    alert('AI recipe saved as "' + data.title + '"')
  } catch (e) {
    console.error('Save AI recipe failed', e)
    alert(e?.response?.data?.detail || 'Save failed')
  }
}
</script>
