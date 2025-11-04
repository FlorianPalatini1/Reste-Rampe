<template>
  <div class="px-4 py-6 sm:px-0">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-3xl font-bold text-gray-900">{{ t('ingredients.title') }}</h2>
      <button
        @click="showAddModal = true"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
      >
        + {{ t('ingredients.add') }}
      </button>
    </div>

    <!-- Filter Tabs -->
    <div class="mb-6 border-b border-gray-200">
      <nav class="-mb-px flex space-x-8">
        <button
          @click="filterLocation = null"
          :class="filterLocation === null ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
          class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
        >
          {{ t('common.loading') === 'Loading...' ? `All (${ingredients.length})` : `All (${ingredients.length})` }}
        </button>
        <button
          @click="filterLocation = 'Fridge'"
          :class="filterLocation === 'Fridge' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
          class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
        >
          ❄️ {{ t('ingredients.fridge') }}
        </button>
        <button
          @click="filterLocation = 'Pantry'"
          :class="filterLocation === 'Pantry' ? 'border-primary-500 text-primary-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
          class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
        >
          🗄️ {{ t('ingredients.pantry') }}
        </button>
      </nav>
    </div>

    <!-- Ingredients List -->
    <div class="bg-white shadow overflow-hidden sm:rounded-md">
      <ul class="divide-y divide-gray-200">
        <li v-for="ingredient in filteredIngredients" :key="ingredient.id" class="hover:bg-gray-50">
          <div class="px-4 py-4 sm:px-6">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <h3 class="text-lg font-medium text-gray-900">{{ ingredient.name }}</h3>
                <div class="mt-2 flex items-center text-sm text-gray-500 space-x-4">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                    {{ getCategoryIcon(ingredient.category) }} {{ ingredient.category }}
                  </span>
                  <span 
                    :class="[
                      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                      getLocationColorClass(ingredient.location)
                    ]"
                  >
                    {{ getLocationIcon(ingredient.location) }} {{ getLocationLabel(ingredient.location) }}
                  </span>
                  <span>{{ t('ingredients.quantity') }}: {{ ingredient.quantity }} {{ ingredient.unit }}</span>
                  <span v-if="ingredient.expiry_date" :class="isExpiringSoon(ingredient.expiry_date) ? 'text-red-600 font-semibold' : ''">
                    {{ t('ingredients.expiryDate') }}: {{ formatDate(ingredient.expiry_date) }}
                  </span>
                </div>
              </div>
              <div class="flex space-x-2">
                <button
                  @click="editIngredient(ingredient)"
                  class="inline-flex items-center px-3 py-1.5 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                >
                  {{ t('ingredients.edit') }}
                </button>
                <button
                  @click="deleteIngredientConfirm(ingredient.id)"
                  class="inline-flex items-center px-3 py-1.5 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
                >
                  {{ t('ingredients.delete') }}
                </button>
              </div>
            </div>
          </div>
        </li>
      </ul>
      <div v-if="filteredIngredients.length === 0" class="text-center py-12">
        <p class="text-gray-500">{{ t('ingredients.empty') }}</p>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal || editingIngredient" class="fixed z-10 inset-0 overflow-y-auto">
      <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>
        <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <h3 class="text-lg font-medium text-gray-900 mb-4">
              {{ editingIngredient ? t('ingredients.edit') : t('ingredients.add') }}
            </h3>
            <form @submit.prevent="saveIngredient">
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700">{{ t('ingredients.name') }}</label>
                  <input v-model="form.name" type="text" required
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">{{ t('ingredients.category') }}</label>
                  <select v-model="form.category" required
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500">
                    <option value="Vegetables">{{ t('ingredients.categories.vegetables') }}</option>
                    <option value="Fruits">{{ t('ingredients.categories.fruits') }}</option>
                    <option value="Dairy">{{ t('ingredients.categories.dairy') }}</option>
                    <option value="Meat">{{ t('ingredients.categories.meat') }}</option>
                    <option value="Grains">{{ t('ingredients.categories.grains') }}</option>
                    <option value="Beverages">{{ t('ingredients.categories.beverages') }}</option>
                    <option value="Condiments">{{ t('ingredients.categories.condiments') }}</option>
                    <option value="Other">{{ t('ingredients.categories.other') }}</option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">{{ t('ingredients.location') }}</label>
                  <select v-model="form.location" required
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500">
                    <option value="Fridge">{{ t('ingredients.fridge') }}</option>
                    <option value="Pantry">{{ t('ingredients.pantry') }}</option>
                  </select>
                </div>
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700">{{ t('ingredients.quantity') }}</label>
                    <input v-model.number="form.quantity" type="number" step="0.1" required
                      class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500">
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700">{{ t('ingredients.unit') }}</label>
                    <select v-model="form.unit" required
                      class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500">
                      <option>kg</option>
                      <option>g</option>
                      <option>L</option>
                      <option>ml</option>
                      <option>pieces</option>
                      <option>cups</option>
                    </select>
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">{{ t('ingredients.expiryDate') }} ({{ t('ingredients.optional') }})</label>
                  <input v-model="form.expiry_date" type="date"
                    class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500">
                </div>
              </div>
              <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                <button type="submit"
                  class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none sm:col-start-2 sm:text-sm">
                  {{ t('common.save') }}
                </button>
                <button type="button" @click="closeModal"
                  class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none sm:mt-0 sm:col-start-1 sm:text-sm">
                  {{ t('common.cancel') }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { ingredientsAPI } from '../services/api.js'

const { t } = useI18n()

const ingredients = ref([])
const filterLocation = ref(null)
const showAddModal = ref(false)
const editingIngredient = ref(null)
const form = ref({
  name: '',
  category: 'Vegetables',
  location: 'Fridge',
  quantity: 1,
  unit: 'kg',
  expiry_date: null
})

const filteredIngredients = computed(() => {
  if (!filterLocation.value) return ingredients.value
  return ingredients.value.filter(i => i.location === filterLocation.value)
})

const loadIngredients = async () => {
  try {
    const response = await ingredientsAPI.getAll()
    ingredients.value = response.data
  } catch (error) {
    console.error('Error loading ingredients:', error)
  }
}

const saveIngredient = async () => {
  try {
    if (editingIngredient.value) {
      await ingredientsAPI.update(editingIngredient.value.id, form.value)
    } else {
      await ingredientsAPI.create(form.value)
    }
    await loadIngredients()
    closeModal()
  } catch (error) {
    console.error('Error saving ingredient:', error)
    // show backend-provided message if available
    const msg = error?.response?.data?.detail || error.message || 'Error saving ingredient'
    alert(msg)
  }
}

const editIngredient = (ingredient) => {
  editingIngredient.value = ingredient
  form.value = { ...ingredient }
}

const deleteIngredientConfirm = async (id) => {
  if (confirm(t('common.delete') + '?')) {
    try {
      await ingredientsAPI.delete(id)
      await loadIngredients()
    } catch (error) {
      console.error('Error deleting ingredient:', error)
    }
  }
}

const closeModal = () => {
  showAddModal.value = false
  editingIngredient.value = null
  form.value = {
    name: '',
    category: 'Vegetables',
    location: 'Fridge',
    quantity: 1,
    unit: 'kg',
    expiry_date: null
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const isExpiringSoon = (expiryDate) => {
  const today = new Date()
  const expiry = new Date(expiryDate)
  const diffDays = Math.ceil((expiry - today) / (1000 * 60 * 60 * 24))
  return diffDays <= 7 && diffDays >= 0
}

const getLocationLabel = (location) => {
  if (location === 'Fridge') return t('ingredients.fridge')
  if (location === 'Pantry') return t('ingredients.pantry')
  return location
}

const getLocationIcon = (location) => {
  if (location === 'Fridge') return '❄️'
  if (location === 'Pantry') return '🗄️'
  return '📦'
}

const getLocationColorClass = (location) => {
  if (location === 'Fridge') return 'bg-blue-100 text-blue-800'
  if (location === 'Pantry') return 'bg-amber-100 text-amber-800'
  return 'bg-gray-100 text-gray-800'
}

const getCategoryIcon = (category) => {
  const icons = {
    'Vegetables': '🥬',
    'Fruits': '🍎',
    'Dairy': '🧈',
    'Meat': '🥩',
    'Grains': '🌾',
    'Beverages': '🥤',
    'Condiments': '🧂',
    'Other': '📦',
    // German
    'Gemüse': '🥬',
    'Obst': '🍎',
    'Milchprodukte': '🧈',
    'Fleisch': '🥩',
    'Getreide': '🌾',
    'Getränke': '🥤',
    'Würzmittel': '🧂',
    'Blattgemüse': '🥬',
    'Fisch': '🐟',
    'Öle': '🫒',
    'Proteine': '💪',
    'Sonstiges': '📦'
  }
  return icons[category] || '📦'
}

onMounted(() => {
  loadIngredients()
})
</script>
