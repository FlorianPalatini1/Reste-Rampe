import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import i18n from './i18n'
import './assets/tailwind.css'
import './assets/main.css'
import { useAuth } from './stores/auth'
import api from './lib/api'

const app = createApp(App)
app.use(i18n)
app.use(router)
// load token from storage and validate with backend
const { loadFromStorage, setToken, state } = useAuth()
loadFromStorage()
// DEV helper: allow setting token via URL param __dev_token (e.g. ?__dev_token=xxx)
try {
	const params = new URLSearchParams(window.location.search)
	const devToken = params.get('__dev_token')
	if (devToken) {
		// set token in store and localStorage
		setToken(devToken)
		// remove param from URL without reloading the page
		params.delete('__dev_token')
		const newSearch = params.toString()
		const newUrl = window.location.pathname + (newSearch ? ('?' + newSearch) : '') + window.location.hash
		window.history.replaceState({}, '', newUrl)
	}
} catch (e) {
	// ignore in non-browser contexts
}
if (state.token) {
	// try to populate user
	api.get('/auth/me').then(resp => {
		state.user = resp.data
	}).catch(() => {
		// invalid token
		setToken(null)
	})
}
app.mount('#app')
