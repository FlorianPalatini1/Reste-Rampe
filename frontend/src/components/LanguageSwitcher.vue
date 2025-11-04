<template>
  <div class="flex items-center gap-2">
    <label class="text-sm font-medium text-gray-700">
      {{ t('app.language') }}:
    </label>
    <div class="flex items-center gap-2">
      <select
        v-model="locale"
        class="px-3 py-1 border border-gray-300 rounded-md text-sm font-medium hover:border-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="de">Deutsch</option>
        <option value="en">English</option>
        <option value="fr">Français</option>
        <option value="ja">日本語</option>
        <option value="tr">Türkçe</option>
        <option value="fa">فارسی</option>
        <option value="nds">Plattdeutsch</option>
      </select>
      <span class="text-sm text-gray-600">{{ currentLangName }}</span>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { watch, computed } from 'vue'

const i18n = useI18n()
const { t } = i18n

const LANG_NAMES = { de: 'Deutsch', en: 'English', fr: 'Français', ja: '日本語', tr: 'Türkçe', fa: 'فارسی', nds: 'Plattdeutsch' }
const currentLangName = computed(() => LANG_NAMES[i18n.locale.value] || i18n.locale.value)

// expose a v-model friendly computed binding for the select
const locale = computed({
  get: () => i18n.locale.value,
  set: (val) => {
    if (!val || val === i18n.locale.value) return
    i18n.locale.value = val
    // persist to localStorage and update document lang
    try { localStorage.setItem('locale', val) } catch (e) {}
    try { document.documentElement.lang = val } catch (e) {}
    // for RTL languages like Persian, set document direction
    try { document.documentElement.dir = (val === 'fa') ? 'rtl' : 'ltr' } catch (e) {}
  }
})

// Keep document lang in sync if something else updates the locale
watch(
  () => i18n.locale.value,
  (newLocale) => {
    try { localStorage.setItem('locale', newLocale) } catch (e) {}
    try { document.documentElement.lang = newLocale } catch (e) {}
  }
)
</script>
