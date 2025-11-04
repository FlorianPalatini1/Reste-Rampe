import { createI18n } from 'vue-i18n'
import de from './locales/de.json'
import en from './locales/en.json'
import fr from './locales/fr.json'
import ja from './locales/ja.json'
import tr from './locales/tr.json'
import fa from './locales/fa.json'
import nds from './locales/nds.json'

// Determine locale from localStorage or browser language
const getInitialLocale = () => {
  const saved = localStorage.getItem('locale')
  if (saved) return saved
  
  // Browser language
  const browserLang = navigator.language.split('-')[0]
  return ['de', 'en', 'fr', 'ja', 'tr', 'fa', 'nds'].includes(browserLang) ? browserLang : 'de'
}

const i18n = createI18n({
  legacy: false, // Composition API mode
  locale: getInitialLocale(),
  fallbackLocale: 'de',
  messages: {
    de,
    en,
    fr,
    ja,
    tr,
    fa,
    nds
  }
})

export default i18n
