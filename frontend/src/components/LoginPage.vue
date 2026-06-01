<template>
  <div class="login-page">

    <!-- ══ LEFT PANEL – branding ══ -->
    <div class="login-left" ref="leftRef">
      <!-- Background blobs -->
      <div class="left-blobs" aria-hidden="true">
        <div class="lb lb--1"></div>
        <div class="lb lb--2"></div>
        <div class="lb lb--3"></div>
      </div>

      <!-- Noise texture -->
      <div class="left-noise" aria-hidden="true"></div>

      <!-- Content -->
      <div class="left-content">
        <!-- Logo -->
        <RouterLink to="/" class="left-logo-link">
          <AppLogo :icon-size="42" :font-size="22" :gap="12" text-color="white" />
        </RouterLink>

        <!-- Main copy -->
        <div class="left-copy">
          <h2 class="left-title">
            Gérez vos équipes<br>
            <span class="left-title-shine">sans friction.</span>
          </h2>
          <p class="left-sub">
            La plateforme RH qui centralise planning, temps de travail, paie et admin pour les équipes de terrain.
          </p>
        </div>

        <!-- Feature highlights -->
        <ul class="left-features">
          <li v-for="f in features" :key="f.text">
            <div class="left-feat-icon" :style="{ background: f.bg }">
              <v-icon size="14" color="white">{{ f.icon }}</v-icon>
            </div>
            <span>{{ f.text }}</span>
          </li>
        </ul>

        <!-- Social proof -->
        <div class="left-proof">
          <div class="proof-avatars">
            <img v-for="n in 4" :key="n" :src="`https://i.pravatar.cc/28?img=${n + 14}`" class="proof-avatar" alt=""
              loading="lazy">
          </div>
          <div class="proof-text">
            <div class="proof-stars">
              <svg v-for="n in 5" :key="n" width="13" height="13" viewBox="0 0 24 24" fill="#FBBF24">
                <path
                  d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
              </svg>
            </div>
            <span>4,5/5 · <strong>25 000+</strong> équipes</span>
          </div>
        </div>
      </div>

      <!-- Bottom quote -->
      <div class="left-quote">
        <p>"TimeApp nous a fait gagner 3 heures par semaine sur la préparation des plannings."</p>
        <div class="quote-author">
          <img src="https://i.pravatar.cc/32?img=47" alt="Sophie M." class="quote-avatar" loading="lazy">
          <span>Sophie M. — Directrice RH, Brasserie des Prés</span>
        </div>
      </div>
    </div>

    <!-- ══ RIGHT PANEL – form ══ -->
    <div class="login-right" ref="rightRef">
      <!-- Back to home -->
      <RouterLink to="/" class="back-link">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
          <path d="M19 12H5M12 19l-7-7 7-7" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
        </svg>
        Retour à l'accueil
      </RouterLink>

      <div class="form-container">
        <!-- Mobile logo (hidden on desktop) -->
        <div class="form-logo-mobile">
          <AppLogo :icon-size="36" :font-size="19" :gap="10" />
        </div>

        <!-- Heading -->
        <div class="form-header">
          <h1 class="form-title">Bon retour 👋</h1>
          <p class="form-sub">
            Pas encore de compte ?
            <RouterLink to="/" class="form-sub-link">Essai gratuit 14 jours</RouterLink>
          </p>
        </div>

        <!-- SSO buttons -->
        <div class="sso-group">
          <button class="sso-btn" @click="loginWithGoogle">
            <svg width="18" height="18" viewBox="0 0 24 24">
              <path fill="#4285F4"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
              <path fill="#34A853"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
              <path fill="#FBBC05"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
              <path fill="#EA4335"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
            </svg>
            Continuer avec Google
          </button>
          <button class="sso-btn" @click="loginWithMicrosoft">
            <svg width="18" height="18" viewBox="0 0 24 24">
              <path fill="#F25022" d="M11.4 2H2v9.4h9.4V2z" />
              <path fill="#7FBA00" d="M22 2h-9.4v9.4H22V2z" />
              <path fill="#00A4EF" d="M11.4 12.6H2V22h9.4v-9.4z" />
              <path fill="#FFB900" d="M22 12.6h-9.4V22H22v-9.4z" />
            </svg>
            Continuer avec Microsoft
          </button>
        </div>

        <!-- Divider -->
        <div class="form-divider">
          <span>ou continuer avec email</span>
        </div>

        <!-- Form -->
        <form class="login-form" @submit.prevent="handleSubmit" novalidate>
          <!-- Email -->
          <div class="field-group">
            <label class="field-label" for="email">Adresse email</label>
            <div :class="['field-wrap', { error: errors.email, focused: focusedField === 'email' }]">
              <div class="field-icon">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"
                    stroke="currentColor" stroke-width="1.8" />
                  <polyline points="22,6 12,13 2,6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
                </svg>
              </div>
              <input id="email" v-model="form.email" type="email" placeholder="vous@entreprise.com" class="field-input"
                autocomplete="email" @focus="focusedField = 'email'" @blur="focusedField = null; validateEmail()">
            </div>
            <span v-if="errors.email" class="field-error">{{ errors.email }}</span>
          </div>

          <!-- Password -->
          <div class="field-group">
            <div class="field-label-row">
              <label class="field-label" for="password">Mot de passe</label>
              <a href="#" class="forgot-link">Mot de passe oublié ?</a>
            </div>
            <div :class="['field-wrap', { error: errors.password, focused: focusedField === 'password' }]">
              <div class="field-icon">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="currentColor" stroke-width="1.8" />
                  <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
                </svg>
              </div>
              <input id="password" v-model="form.password" :type="showPass ? 'text' : 'password'" placeholder="••••••••"
                class="field-input" autocomplete="current-password" @focus="focusedField = 'password'"
                @blur="focusedField = null; validatePassword()">
              <button type="button" class="pass-toggle" @click="showPass = !showPass"
                :aria-label="showPass ? 'Masquer' : 'Afficher'">
                <svg v-if="!showPass" width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" stroke="currentColor" stroke-width="1.8" />
                  <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.8" />
                </svg>
                <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path
                    d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"
                    stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
                  <line x1="1" y1="1" x2="23" y2="23" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" />
                </svg>
              </button>
            </div>
            <span v-if="errors.password" class="field-error">{{ errors.password }}</span>
          </div>

          <!-- Remember me -->
          <div class="remember-row">
            <label class="check-label">
              <input type="checkbox" v-model="form.remember" class="check-input">
              <span class="check-box">
                <svg v-if="form.remember" width="10" height="10" viewBox="0 0 24 24" fill="none">
                  <path d="M20 6L9 17l-5-5" stroke="white" stroke-width="3" stroke-linecap="round"
                    stroke-linejoin="round" />
                </svg>
              </span>
              <span class="check-text">Se souvenir de moi</span>
            </label>
          </div>

          <!-- Submit -->
          <button type="submit" :class="['submit-btn', { loading: isLoading }]" :disabled="isLoading">
            <span v-if="!isLoading" class="submit-btn__text">
              Se connecter
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                  stroke-linejoin="round" />
              </svg>
            </span>
            <span v-else class="submit-btn__loader">
              <svg class="spin" width="18" height="18" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="rgba(255,255,255,0.3)" stroke-width="3" />
                <path d="M12 2a10 10 0 0 1 10 10" stroke="white" stroke-width="3" stroke-linecap="round" />
              </svg>
              Connexion en cours…
            </span>
          </button>

          <!-- Error global -->
          <Transition name="fade">
            <div v-if="globalError" class="global-error">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" />
                <line x1="12" y1="8" x2="12" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                <line x1="12" y1="16" x2="12.01" y2="16" stroke="currentColor" stroke-width="2"
                  stroke-linecap="round" />
              </svg>
              {{ globalError }}
            </div>
          </Transition>
        </form>

        <!-- Footer links -->
        <div class="form-footer">
          <span>En vous connectant vous acceptez nos</span>
          <a href="#">Conditions d'utilisation</a>
          <span>et notre</span>
          <a href="#">Politique de confidentialité</a>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import AppLogo from './AppLogo.vue'
import gsap from 'gsap'
import { useAuthStore } from '../stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({ email: '', password: '', remember: false })
const errors = ref({ email: '', password: '' })
const globalError = ref('')
const isLoading = ref(false)
const showPass = ref(false)
const focusedField = ref(null)

const features = [
  { icon: 'mdi-calendar-month-outline', text: 'Planning intelligent en 1 clic', bg: '#6366F1' },
  { icon: 'mdi-clock-time-four-outline', text: 'Suivi temps & absences en temps réel', bg: '#10B981' },
  { icon: 'mdi-cash-multiple', text: 'Paie préparée automatiquement', bg: '#F97316' },
  { icon: 'mdi-shield-check-outline', text: 'Conforme RGPD & droit du travail', bg: '#A855F7' },
]

const validateEmail = () => {
  const v = form.value.email
  if (!v) { errors.value.email = 'L\'adresse email est requise'; return false }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) { errors.value.email = 'Adresse email invalide'; return false }
  errors.value.email = ''
  return true
}

const validatePassword = () => {
  if (!form.value.password) { errors.value.password = 'Le mot de passe est requis'; return false }
  if (form.value.password.length < 6) { errors.value.password = 'Minimum 6 caractères'; return false }
  errors.value.password = ''
  return true
}

const handleSubmit = async () => {
  const eOk = validateEmail()
  const pOk = validatePassword()
  if (!eOk || !pOk) return

  isLoading.value = true
  globalError.value = ''
  try {
    await authStore.login(form.value.email, form.value.password)
  } catch {
    globalError.value = 'Email ou mot de passe incorrect. Veuillez réessayer.'
  } finally {
    isLoading.value = false
  }
}

const loginWithGoogle = () => { router.push('/dashboard') }
const loginWithMicrosoft = () => { router.push('/dashboard') }

const leftRef = ref(null)
const rightRef = ref(null)
onMounted(() => {
  gsap.from(leftRef.value, { x: -40, opacity: 0, duration: 0.9, ease: 'power3.out' })
  gsap.from(rightRef.value, { x: 40, opacity: 0, duration: 0.9, ease: 'power3.out', delay: 0.1 })
  gsap.from('.form-header, .sso-group, .form-divider, .login-form, .form-footer', {
    y: 20, opacity: 0, duration: 0.6, stagger: 0.08, ease: 'power3.out', delay: 0.35
  })
})
</script>

<style scoped>
/* ── Reset ── */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.login-page {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 100vh;
  font-family: 'Plus Jakarta Sans', 'Inter', system-ui, sans-serif;
  overflow: hidden;
}

/* ══════════ LEFT PANEL ══════════ */
.login-left {
  background: linear-gradient(145deg, #1E1B4B 0%, #312E81 40%, #1E1B4B 100%);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  padding: 40px 48px;
  min-height: 100vh;
}

/* Blobs */
.left-blobs {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.lb {
  position: absolute;
  border-radius: 50%;
  filter: blur(70px);
}

.lb--1 {
  width: 350px;
  height: 350px;
  background: rgba(99, 102, 241, 0.3);
  top: -80px;
  left: -80px;
  animation: lbFloat 9s ease-in-out infinite;
}

.lb--2 {
  width: 280px;
  height: 280px;
  background: rgba(124, 58, 237, 0.25);
  bottom: 80px;
  right: -60px;
  animation: lbFloat 11s ease-in-out infinite reverse;
}

.lb--3 {
  width: 200px;
  height: 200px;
  background: rgba(16, 185, 129, 0.12);
  top: 50%;
  left: 50%;
  animation: lbFloat 7s ease-in-out infinite 2s;
}

@keyframes lbFloat {

  0%,
  100% {
    transform: translate(0, 0)
  }

  50% {
    transform: translate(20px, -20px)
  }
}

/* Noise */
.left-noise {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  opacity: 0.04;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  background-size: 180px;
}

.left-content {
  position: relative;
  z-index: 2;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.left-logo-link {
  text-decoration: none;
  display: inline-block;
  width: fit-content;
}

.left-copy {}

.left-title {
  font-size: clamp(1.8rem, 2.8vw, 2.4rem);
  font-weight: 900;
  line-height: 1.18;
  color: white;
  margin-bottom: 16px;
}

.left-title-shine {
  background: linear-gradient(90deg, #A5B4FC, #DDD6FE, #C4B5FD);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.left-sub {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.65;
  max-width: 360px;
}

/* Features list */
.left-features {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.left-features li {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 0.88rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.8);
}

.left-feat-icon {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  opacity: 0.9;
}

/* Social proof */
.left-proof {
  display: flex;
  align-items: center;
  gap: 12px;
}

.proof-avatars {
  display: flex;
}

.proof-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.3);
  margin-left: -7px;
  object-fit: cover;
}

.proof-avatar:first-child {
  margin-left: 0;
}

.proof-text {
  font-size: 0.78rem;
  color: rgba(255, 255, 255, 0.6);
}

.proof-stars {
  display: flex;
  gap: 1px;
  margin-bottom: 2px;
}

.proof-text strong {
  color: white;
}

/* Bottom quote */
.left-quote {
  position: relative;
  z-index: 2;
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 18px 20px;
}

.left-quote p {
  font-size: 0.83rem;
  color: rgba(255, 255, 255, 0.75);
  line-height: 1.6;
  font-style: italic;
  margin-bottom: 12px;
}

.quote-author {
  display: flex;
  align-items: center;
  gap: 9px;
}

.quote-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.2);
  object-fit: cover;
}

.quote-author span {
  font-size: 0.75rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.6);
}

/* ══════════ RIGHT PANEL ══════════ */
.login-right {
  background: #FAFAFA;
  display: flex;
  flex-direction: column;
  padding: 32px 40px;
  min-height: 100vh;
  overflow-y: auto;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  font-size: 0.83rem;
  font-weight: 600;
  color: #71717A;
  text-decoration: none;
  width: fit-content;
  transition: color 0.2s;
  margin-bottom: 8px;
}

.back-link:hover {
  color: #4F46E5;
}

.form-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  max-width: 420px;
  margin: 0 auto;
  width: 100%;
  padding: 24px 0 48px;
}

.form-logo-mobile {
  display: none;
  margin-bottom: 32px;
}

.form-header {
  margin-bottom: 28px;
}

.form-title {
  font-size: 1.9rem;
  font-weight: 900;
  color: #09090B;
  margin-bottom: 8px;
  line-height: 1.2;
}

.form-sub {
  font-size: 0.875rem;
  color: #71717A;
  display: flex;
  align-items: center;
  gap: 5px;
  flex-wrap: wrap;
}

.form-sub-link {
  color: #4F46E5;
  font-weight: 700;
  text-decoration: none;
  transition: color 0.2s;
}

.form-sub-link:hover {
  color: #4338CA;
  text-decoration: underline;
}

/* SSO */
.sso-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.sso-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  padding: 11px 16px;
  background: white;
  border: 1.5px solid #E4E4E7;
  border-radius: 12px;
  font-size: 0.83rem;
  font-weight: 600;
  color: #18181B;
  cursor: pointer;
  transition: all 0.2s;
}

.sso-btn:hover {
  border-color: #A1A1AA;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  background: #FAFAFA;
}

/* Divider */
.form-divider {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 24px;
  color: #A1A1AA;
  font-size: 0.78rem;
  font-weight: 500;
}

.form-divider::before,
.form-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: #E4E4E7;
}

/* Form fields */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.field-label {
  font-size: 0.82rem;
  font-weight: 700;
  color: #3F3F46;
}

.forgot-link {
  font-size: 0.78rem;
  font-weight: 600;
  color: #4F46E5;
  text-decoration: none;
  transition: color 0.2s;
}

.forgot-link:hover {
  color: #4338CA;
}

.field-wrap {
  display: flex;
  align-items: center;
  background: white;
  border: 1.5px solid #E4E4E7;
  border-radius: 12px;
  transition: border-color 0.2s, box-shadow 0.2s;
  overflow: hidden;
}

.field-wrap.focused {
  border-color: #4F46E5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.field-wrap.error {
  border-color: #EF4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.08);
}

.field-icon {
  padding: 0 12px;
  color: #A1A1AA;
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

.field-wrap.focused .field-icon {
  color: #4F46E5;
}

.field-input {
  flex: 1;
  padding: 12px 12px 12px 0;
  border: none;
  outline: none;
  background: none;
  font-size: 0.9rem;
  color: #18181B;
  font-family: inherit;
}

.field-input::placeholder {
  color: #A1A1AA;
}

.pass-toggle {
  padding: 0 12px;
  background: none;
  border: none;
  cursor: pointer;
  color: #A1A1AA;
  display: flex;
  align-items: center;
  transition: color 0.2s;
  flex-shrink: 0;
}

.pass-toggle:hover {
  color: #52525B;
}

.field-error {
  font-size: 0.75rem;
  color: #EF4444;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Remember me */
.remember-row {
  margin: -4px 0;
}

.check-label {
  display: flex;
  align-items: center;
  gap: 9px;
  cursor: pointer;
  user-select: none;
}

.check-input {
  display: none;
}

.check-box {
  width: 18px;
  height: 18px;
  border: 1.5px solid #D4D4D8;
  border-radius: 5px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
  flex-shrink: 0;
}

.check-input:checked+.check-box {
  background: #4F46E5;
  border-color: #4F46E5;
}

.check-text {
  font-size: 0.83rem;
  font-weight: 500;
  color: #52525B;
}

/* Submit button */
.submit-btn {
  width: 100%;
  padding: 14px;
  background: #4F46E5;
  color: white;
  border: none;
  border-radius: 13px;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
  box-shadow: 0 4px 16px rgba(79, 70, 229, 0.35);
  margin-top: 4px;
  font-family: inherit;
}

.submit-btn:hover:not(:disabled) {
  background: #4338CA;
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(79, 70, 229, 0.45);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.8;
  cursor: not-allowed;
}

.submit-btn__text,
.submit-btn__loader {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.spin {
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Global error */
.global-error {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 14px;
  background: #FEF2F2;
  border: 1px solid #FECACA;
  border-radius: 10px;
  font-size: 0.83rem;
  font-weight: 500;
  color: #DC2626;
}

/* Form footer */
.form-footer {
  margin-top: 24px;
  font-size: 0.75rem;
  color: #A1A1AA;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  flex-wrap: wrap;
  line-height: 1.6;
}

.form-footer a {
  color: #71717A;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}

.form-footer a:hover {
  color: #4F46E5;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

/* ══════════ RESPONSIVE ══════════ */
@media (max-width: 900px) {
  .login-page {
    grid-template-columns: 1fr;
  }

  .login-left {
    display: none;
  }

  .login-right {
    padding: 24px;
    min-height: 100vh;
  }

  .form-logo-mobile {
    display: flex;
    justify-content: center;
  }

  .form-container {
    padding: 0 0 40px;
  }
}

@media (max-width: 480px) {
  .login-right {
    padding: 20px 16px;
  }

  .sso-group {
    flex-direction: column;
  }

  .form-title {
    font-size: 1.5rem;
  }
}
</style>
