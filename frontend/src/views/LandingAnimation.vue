
<template>
  <div class="landing-root">
    <div class="paper">
      <header class="masthead">
        <h1 class="masthead-hero">FOOD NEWS TODAY</h1>
        <p class="masthead-sub">Reste Rampe — Die interaktive "Zeitung" für nachhaltiges Kochen</p>
      </header>

      <section class="hero">
        <div class="hero-video-wrap">
          <video
            ref="heroVideo"
            class="hero-video"
            :src="`/landing.mp4?v=${Date.now()}`"
            playsinline
            muted
            autoplay
            preload="metadata"
            @loadedmetadata="onLoadedMetadata"
            @canplay="onCanPlay"
            @playing="onPlaying"
            @ended="onEnded"
            @error="onError"
          ></video>
        </div>

        <div class="hero-controls">
          <!-- Only show Skip button which navigates to the login page -->
          <button v-if="!entered" @click="skipToLogin" class="skip-btn">Skip</button>
        </div>
      </section>

      <footer class="byline">© {{ new Date().getFullYear() }} Reste Rampe</footer>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const heroVideo = ref(null)
const entered = ref(false)

function enterSite() {
  entered.value = true
  // Smoothly pause the video and navigate
  if (heroVideo.value && !heroVideo.value.paused) {
    heroVideo.value.pause()
  }
  // small timeout for UX smoothness
  setTimeout(() => router.push({ name: 'dashboard' }), 150)
}

function skipVideo() {
  entered.value = true
  if (heroVideo.value) heroVideo.value.pause()
  router.push({ name: 'dashboard' })
}

// New helper to skip directly to the login page (not dashboard)
function skipToLogin() {
  entered.value = true
  if (heroVideo.value) heroVideo.value.pause()
  router.push({ name: 'login' })
}

function onLoadedMetadata() {
  // Video metadata loaded - now safe to play
  console.log('Video metadata loaded')
  if (heroVideo.value) {
    heroVideo.value.play().catch(err => console.log('Autoplay prevented:', err))
  }
}

function onCanPlay() {
  // Video can now play
  console.log('Video can play')
  if (heroVideo.value && heroVideo.value.paused) {
    heroVideo.value.play().catch(err => console.log('Play failed:', err))
  }
}

function onPlaying() {
  // Video is now playing
  console.log('Video is playing')
}

function onError(event) {
  // Video error
  console.error('Video error:', event)
  console.error('Error code:', heroVideo.value?.error?.code)
}

function onEnded() {
  // when video ends, automatically enter
  if (!entered.value) enterSite()
}

onMounted(() => {
  // small precaution: ensure video muted for autoplay
  if (heroVideo.value) heroVideo.value.muted = true
})
</script>

<style scoped>
/* Paper background */
.landing-root {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f6efe6; /* light paper */
  padding: 3rem 1rem;
}
.paper {
  width: 100%;
  max-width: 1100px;
  background: linear-gradient(180deg, #fffdf9 0%, #fbf7f1 100%);
  border: 1px solid #e6ded2;
  box-shadow: 0 10px 30px rgba(30,20,10,0.08);
  padding: 2.5rem;
  font-family: 'Playfair Display', Georgia, 'Times New Roman', serif;
}

/* Masthead */
.masthead { text-align: center; margin-bottom: 1.25rem }
.masthead-hero {
  font-size: 4.75rem; /* large masthead */
  line-height: 1;
  margin: 0;
  color: #1a1a1a;
  letter-spacing: -0.02em;
  text-transform: uppercase;
  font-weight: 700;
}
.masthead-sub {
  margin-top: 0.5rem;
  color: #5a4f43;
  font-size: 1.125rem;
}

/* Hero area */
.hero { display: flex; flex-direction: column; align-items: center; gap: 1rem }
.hero-video-wrap { 
  width: 100%; 
  border: 6px solid #efe6d9; 
  box-shadow: inset 0 0 0 1px rgba(0,0,0,0.02);
  aspect-ratio: 16 / 9;
  overflow: hidden;
  background: #f0f0f0;
}
.hero-video { 
  width: 100%; 
  height: 100%; 
  display: block; 
  border-radius: 2px;
  object-fit: contain;
}

.hero-controls { margin-top: 0.75rem; display: flex; gap: 0.5rem }
.enter-btn, .skip-btn {
  padding: 0.6rem 1rem;
  border-radius: 6px;
  border: 1px solid rgba(0,0,0,0.08);
  background: white;
  cursor: pointer;
  font-weight: 600;
}
.enter-btn { color: #1a1a1a }
.skip-btn { color: #666 }

.byline { text-align: center; margin-top: 1.25rem; color: #938679; font-size: 0.9rem }

@media (max-width: 640px) {
  .masthead-hero { font-size: 2.25rem }
}
</style>

