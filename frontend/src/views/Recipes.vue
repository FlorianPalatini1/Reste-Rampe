<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-3xl font-bold text-gray-900">{{ t('recipes.title') }}</h2>
      <div class="flex space-x-3">
        <button
          @click="findMatchingRecipes"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700"
        >
          🔍 {{ t('recipes.findWithAvailable') }}
        </button>
        <input
          v-model="dietary"
          type="text"
          :placeholder="t('recipes.dietary')"
          class="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 w-80"
        />
        <button
          @click="generateAIRecipe"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-emerald-600 hover:bg-emerald-700"
        >
          🤖 {{ t('recipes.generateAI') }}
        </button>
        <button
          @click="seedSampleRecipes"
          class="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
        >
          📚 {{ t('recipes.loadSample') }}
        </button>
      </div>
    </div>

    <!-- Filter -->
    <div class="mb-6">
      <button
        @click="showHealthyOnly = !showHealthyOnly"
        :class="showHealthyOnly ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'"
        class="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium"
      >
        {{ showHealthyOnly ? '✓' : '' }} {{ t('recipes.healthyOnly') }}
      </button>
    </div>

    <!-- Matching Recipes Alert -->
    <div v-if="showMatchingOnly" class="bg-green-50 border-l-4 border-green-400 p-4 mb-6">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-sm text-green-700">
            {{ t('recipes.showingMatching') }}
            <button @click="showMatchingOnly = false" class="font-medium underline">{{ t('recipes.showAllRecipes') }}</button>
          </p>
        </div>
      </div>
        <div class="flex items-center">
          <span class="icon-sepia">📚</span>
        </div>
    </div>

    <!-- Recipes Grid -->
    <div class="mb-6 bg-gradient-to-r from-green-50 to-emerald-50 rounded-lg shadow-lg p-8 border-2 border-emerald-200" :style="{ display: isGeneratingRecipe ? 'block' : 'none' }">
      <div class="flex items-center justify-center py-16">
        <div class="text-center">
          <div class="mb-6">
            <svg class="animate-spin mx-auto h-16 w-16 text-emerald-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
          <p class="text-lg text-emerald-700 font-semibold">{{ t('common.loading') || 'Rezept wird generiert...' }}</p>
          <p class="text-sm text-gray-600 mt-2">Das kann 5-15 Sekunden dauern ⏳</p>
        </div>
      </div>
    </div>

    <div v-if="aiRecipe" class="mb-6 bg-white rounded-lg shadow p-6">
      <h3 class="text-xl font-semibold mb-1">{{ t('recipes.aiRecipeSuggestion') }}</h3>
      <div v-if="aiModel" class="text-xs text-gray-500 mb-2">{{ t('recipes.model') }}: {{ aiModel }}</div>
      <div class="prose prose-sm max-w-none" v-html="aiHtml"></div>
      <div class="mt-4 flex items-center space-x-2">
        <input v-model="aiTitle" type="text" :placeholder="t('recipes.recipeTitle')"
               class="border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500">
        <button @click="saveAIRecipe"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700">
          {{ t('recipes.saveRecipe') }}
        </button>
      </div>
    </div>

    <!-- Recent AI Suggestions -->
    <div class="mb-6 bg-white rounded-lg shadow p-6">
      <div class="flex items-center justify-between mb-3">
        <h3 class="text-lg font-semibold">{{ t('recipes.aiSuggestions') }}</h3>
        <button @click="loadAISuggestions" class="text-sm text-primary-700 hover:underline">{{ t('recipes.refresh') }}</button>
      </div>
      <ul class="divide-y divide-gray-200">
        <li v-for="s in aiSuggestions" :key="s.id" class="py-3">
          <div class="text-xs text-gray-500 mb-1">{{ new Date(s.created_at).toLocaleString() }}<span v-if="s.dietary"> · {{ s.dietary }}</span></div>
          <div class="text-gray-800 mb-2 max-h-16 overflow-hidden whitespace-pre-wrap">{{ s.text }}</div>
          <button @click="useSuggestion(s.text)" class="text-sm text-emerald-700 hover:underline">{{ t('recipes.useThis') }}</button>
        </li>
        <li v-if="aiSuggestions.length === 0" class="py-3 text-gray-500">{{ t('recipes.noSuggestions') }}</li>
      </ul>
    </div>

    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="recipe in displayedRecipes" :key="recipe.id" class="bg-white overflow-hidden shadow rounded-lg hover:shadow-xl transition-shadow">
        <div class="p-6">
          <div class="flex items-center justify-between mb-3">
            <h3 class="text-xl font-semibold text-gray-900">{{ recipe.name }}</h3>
            <span v-if="recipe.is_healthy" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
              {{ t('recipes.healthyBadge') }}
            </span>
          </div>
          
          <p class="text-gray-600 text-sm mb-4">{{ recipe.description }}</p>
          
          <div class="space-y-2 mb-4">
            <div class="flex items-center text-sm text-gray-500">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span class="icon-sepia">⏱️</span> {{ t('recipes.prepTime') }}: {{ recipe.prep_time }} min
            </div>
            <div class="flex items-center text-sm text-gray-500">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <span class="icon-sepia">👥</span> {{ t('recipes.servings') }}: {{ recipe.servings }}
            </div>
            <div v-if="recipe.calories" class="flex items-center text-sm text-gray-500">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <span class="icon-sepia">🔥</span> {{ t('recipes.calories') }}: {{ recipe.calories }}
            </div>
          </div>

          <div class="flex gap-2 mt-4">
            <button
              @click="viewRecipe(recipe)"
              class="flex-1 inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
            >
              {{ t('recipes.viewRecipe') }}
            </button>
            <button
              @click="deleteRecipe(recipe)"
              class="px-3 py-2 border border-red-300 text-sm font-medium rounded-md text-red-700 bg-red-50 hover:bg-red-100"
              title="Rezept löschen"
            >
              🗑️
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="displayedRecipes.length === 0" class="text-center py-12 bg-white rounded-lg shadow">
      <p class="text-gray-500">{{ t('recipes.noRecipes') }}</p>
    </div>

    <!-- Recipe Detail Modal -->
    <div v-if="selectedRecipe" class="fixed z-10 inset-0 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="flex justify-between items-start mb-4">
              <div>
                <h3 class="text-2xl font-bold text-gray-900">{{ selectedRecipe.name }}</h3>
                <p class="text-gray-600 mt-2">{{ selectedRecipe.description }}</p>
              </div>
              <button @click="selectedRecipe = null" class="text-gray-400 hover:text-gray-500">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div class="mb-6">
              <h4 class="text-lg font-semibold text-gray-900 mb-2">{{ t('recipes.ingredients') }}</h4>
              <ul class="list-disc list-inside space-y-1">
                <li v-for="(ingredient, index) in parseIngredients(selectedRecipe.ingredients)" :key="index" class="text-gray-700">
                  {{ ingredient }}
                </li>
              </ul>
            </div>

            <div>
              <h4 class="text-lg font-semibold text-gray-900 mb-2">{{ t('recipes.instructions') }}</h4>
              <div class="text-gray-700 whitespace-pre-line">{{ selectedRecipe.instructions }}</div>
            </div>

            <div class="mt-6 pt-4 border-t border-gray-200 flex items-center justify-between text-sm text-gray-500">
              <span>⏱️ {{ selectedRecipe.prep_time }} min</span>
              <span>👥 {{ selectedRecipe.servings }} {{ t('recipes.servings') }}</span>
              <span v-if="selectedRecipe.calories">🔥 {{ selectedRecipe.calories }} cal</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { recipesAPI } from '../services/api.js'
import { marked } from 'marked'
import DOMPurify from 'dompurify'

const { t, locale } = useI18n()

const recipes = ref([])
const matchingRecipes = ref([])
const showHealthyOnly = ref(false)
const showMatchingOnly = ref(false)
const selectedRecipe = ref(null)
const aiRecipe = ref('')
const aiTitle = ref('')
const aiModel = ref('')
const dietary = ref('')
const aiSuggestions = ref([])
const isGeneratingRecipe = ref(false)

const aiHtml = computed(() => {
  try {
    const html = marked.parse(aiRecipe.value || '')
    return DOMPurify.sanitize(html)
  } catch {
    return DOMPurify.sanitize(aiRecipe.value || '')
  }
})

const displayedRecipes = computed(() => {
  let filtered = showMatchingOnly.value ? matchingRecipes.value : recipes.value
  if (showHealthyOnly.value && !showMatchingOnly.value) {
    // Only apply healthy filter when NOT in matching mode
    filtered = filtered.filter(r => r.is_healthy)
  }
  return filtered
})

const loadRecipes = async () => {
  try {
    const response = await recipesAPI.getAll()
    recipes.value = response.data
  } catch (error) {
    console.error('Error loading recipes:', error)
  }
}

const saveAIRecipe = async () => {
  try {
    const { data } = await recipesAPI.saveFromAI(aiRecipe.value, aiTitle.value || null)
    aiTitle.value = ''
    aiRecipe.value = ''
    aiModel.value = ''
    // refresh list
    await loadRecipes()
    alert(`${t('recipes.saved')} "${data.name}" ${t('recipes.saved2')}`)
  } catch (e) {
    console.error('Save AI recipe failed', e)
    alert(e?.response?.data?.detail || 'Save failed')
  }
}

const findMatchingRecipes = async () => {
  try {
    isGeneratingRecipe.value = true
    // Ensure UI updates before API call
    await new Promise(resolve => setTimeout(resolve, 100))
    
    const { data } = await recipesAPI.generateFromAvailableIngredients()
    aiRecipe.value = data.text
    aiModel.value = data.model || ''
    aiTitle.value = t('recipes.generatedRecipe')
    showMatchingOnly.value = false
  } catch (error) {
    console.error('Error generating recipe from ingredients:', error)
    aiRecipe.value = error?.response?.data?.detail || t('recipes.generationFailed') || 'Rezept-Generierung fehlgeschlagen'
    aiModel.value = ''
  } finally {
    isGeneratingRecipe.value = false
  }
}

const seedSampleRecipes = async () => {
  try {
    await recipesAPI.seedSample()
    await loadRecipes()
    alert(t('recipes.loadSample') + ' - ' + t('common.success'))
  } catch (error) {
    console.error('Error seeding recipes:', error)
  }
}

const generateAIRecipe = async () => {
  try {
    isGeneratingRecipe.value = true
    // Ensure UI updates before API call
    await new Promise(resolve => setTimeout(resolve, 100))
    
    const response = await recipesAPI.generateFromIngredients(dietary.value || null)
    const { data } = response
    aiRecipe.value = data.text
    aiModel.value = data.model || ''
    if (!aiRecipe.value) {
      aiRecipe.value = t('recipes.generateAI') + ' failed.'
    }
  } catch (e) {
    console.error('AI generation failed', e)
    aiRecipe.value = e?.response?.data?.detail || t('recipes.generateAI') + ' failed.'
    aiModel.value = ''
  } finally {
    isGeneratingRecipe.value = false
  }
}

const viewRecipe = (recipe) => {
  selectedRecipe.value = recipe
}

const deleteRecipe = async (recipe) => {
  if (confirm(`${t('recipes.delete')} "${recipe.name}"?`)) {
    try {
      await recipesAPI.delete(recipe.id)
      await loadRecipes()
      alert(`${recipe.name} ${t('recipes.delete')}`)
    } catch (error) {
      console.error('Error deleting recipe:', error)
      alert('Fehler beim Löschen')
    }
  }
}

const parseIngredients = (ingredientsString) => {
  try {
    return JSON.parse(ingredientsString)
  } catch {
    return []
  }
}

const loadAISuggestions = async () => {
  try {
    const { data } = await recipesAPI.listAISuggestions(5)
    aiSuggestions.value = data
  } catch (e) {
    console.error('Load AI suggestions failed', e)
  }
}

const useSuggestion = (text) => {
  aiRecipe.value = text
  aiModel.value = ''
}

// Watch for language changes and reload recipes
watch(() => locale.value, () => {
  loadRecipes()
})

onMounted(() => {
  loadRecipes()
  loadAISuggestions()
})
</script>
