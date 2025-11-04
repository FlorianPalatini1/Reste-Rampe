import { reactive, computed } from 'vue'

const state = reactive({
  user: null,
  token: null,
})

function setToken(token) {
  state.token = token
  if (token) localStorage.setItem('token', token)
  else localStorage.removeItem('token')
}

function loadFromStorage() {
  const t = localStorage.getItem('token')
  if (t) state.token = t
}

function logout() {
  setToken(null)
  state.user = null
}

const isAuthenticated = computed(() => !!state.token)

function getToken() {
  return state.token
}

function getUser() {
  return state.user
}

export function useAuth() {
  return { state, setToken, loadFromStorage, logout, isAuthenticated, getToken, getUser }
}

export { getToken, isAuthenticated, getUser, setToken, loadFromStorage, logout }
