// Use the shared axios instance which attaches Authorization header from the auth store
import api from '../lib/api'
import i18n from '../i18n'

// Get current language
const getCurrentLanguage = () => {
  return i18n.global.locale.value || 'de'
}

// Ingredients API
export const ingredientsAPI = {
  getAll: (location = null) => {
    const params = location ? { location } : {}
    return api.get('/ingredients/', { params })
  },
  getById: (id) => api.get(`/ingredients/${id}`),
  create: (data) => api.post('/ingredients/', data),
  update: (id, data) => api.put(`/ingredients/${id}`, data),
  delete: (id) => api.delete(`/ingredients/${id}`),
  getExpiringSoon: (days = 7) => api.get('/ingredients/expiring/soon', { params: { days } }),
}

// Shopping Lists API
export const shoppingListsAPI = {
  getAll: () => api.get('/shopping-lists/'),
  getById: (id) => api.get(`/shopping-lists/${id}`),
  create: (data) => api.post('/shopping-lists/', data),
  delete: (id) => api.delete(`/shopping-lists/${id}`),
  addItem: (listId, item) => api.post(`/shopping-lists/${listId}/items`, item),
  updateItem: (itemId, isPurchased) => api.put(`/shopping-lists/items/${itemId}`, null, {
    params: { is_purchased: isPurchased }
  }),
  deleteItem: (itemId) => api.delete(`/shopping-lists/items/${itemId}`),
}

// Recipes API
export const recipesAPI = {
  getAll: (healthyOnly = false) => api.get('/recipes/', { params: { healthy_only: healthyOnly, language: getCurrentLanguage() } }),
  getById: (id) => api.get(`/recipes/${id}`),
  create: (data) => api.post('/recipes/', data),
  delete: (id) => api.delete(`/recipes/${id}`),
  findMatching: () => api.get('/recipes/match/ingredients', { params: { language: getCurrentLanguage() } }),
  generateFromAvailableIngredients: () => api.get('/recipes/match/ingredients', { params: { language: getCurrentLanguage() } }),
  seedSample: () => api.post('/recipes/seed-sample'),
  generateFromIngredients: (dietary = null) => api.post('/recipes/generate', null, { params: { dietary, language: getCurrentLanguage() } }),
  saveFromAI: (text, title = null) => api.post('/recipes/save-from-ai', { text, title }, { params: { language: getCurrentLanguage() } }),
  listAISuggestions: (limit = 5) => api.get('/recipes/ai/suggestions', { params: { limit } }),
}

// News API
export const newsAPI = {
  getAll: (skip = 0, limit = 6, language = null) => api.get('/news/', { params: { skip, limit, language: language || getCurrentLanguage() } }),
  getById: (id) => api.get(`/news/${id}`),
  create: (data) => api.post('/news/', data),
  update: (id, data) => api.put(`/news/${id}`, data),
  delete: (id) => api.delete(`/news/${id}`),
}

export default api
