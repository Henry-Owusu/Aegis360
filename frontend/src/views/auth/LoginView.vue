<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AegisLogo from '@/components/common/AegisLogo.vue'

const router = useRouter()
const authStore = useAuthStore()
const isLoading = ref(false)
const email = ref('')
const errorMessage = ref('')

const ROLE_ROUTES: Record<string, string> = {
  'System Administrator': '/admin/dashboard',
  'DPO': '/modules',
  'PM': '/modules',
  'Approver': '/modules',
}

const handleLogin = async () => {
  if (!email.value) {
    errorMessage.value = 'Please enter an email address.'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    const primaryRole = await authStore.login(email.value)
    const route = ROLE_ROUTES[primaryRole] ?? '/modules'
    router.push(route)
  } catch (err: unknown) {
    if (err instanceof Error) {
      errorMessage.value = err.message
    } else {
      errorMessage.value = 'Login failed. Please check your email and try again.'
    }
  } finally {
    isLoading.value = false
  }
}

const handleHelpClick = () => {
  window.alert('Need assistance? Please contact your Aegis360 System Administrator or IT Helpdesk.')
}
</script>

<template>
  <div class="login-page-container">
    <div class="background-decorations">
      <div class="grid-pattern"></div>
      <div class="glow-orb glow-orb-top-left"></div>
      <div class="glow-orb glow-orb-bottom-right"></div>
    </div>

    <main class="login-content">
      <div class="login-card">
        <div class="card-accent-bar"></div>

        <div class="card-body">
          <header class="card-header">
            <AegisLogo :height="225" />
            <p class="brand-subtitle">SECURE ENTERPRISE GATEWAY</p>
          </header>

          <div class="login-form">
            <div class="input-group">
              <label for="email">Enterprise Email</label>
              <input 
                id="email" 
                v-model="email" 
                type="email" 
                placeholder="e.g. pm@aegis360.com" 
                @keyup.enter="handleLogin"
              />
            </div>
            
            <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>

            <button
              type="button"
              class="sso-button"
              :disabled="isLoading"
              @click="handleLogin"
            >
              <span v-if="isLoading" class="spinner-container">
                <span class="spinner"></span>
                <span>Authenticating...</span>
              </span>
              <template v-else>
                <span class="button-text">Sign In</span>
                <svg class="button-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M5 12h14"></path>
                  <path d="m12 5 7 7-7 7"></path>
                </svg>
              </template>
            </button>
          </div>

          <!-- Enterprise SSO Security Badge -->
          <div class="sso-trust-badge">
            <svg class="lock-shield-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            <span>Single Sign-On (SSO) Enforced</span>
          </div>

          <!-- Card Footer -->
          <footer class="card-footer">
            <div class="security-info">
              <svg class="shield-check-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                <polyline points="9 12 11 14 15 10"></polyline>
              </svg>
              <span>256-bit Encrypted</span>
            </div>

            <a href="#help" class="help-link" @click.prevent="handleHelpClick">
              Need Help?
            </a>
          </footer>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.login-page-container {
  position: relative;
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8fafc;
  background-image: radial-gradient(at 0% 0%, rgba(13, 148, 136, 0.06) 0px, transparent 50%),
                    radial-gradient(at 100% 100%, rgba(15, 23, 42, 0.08) 0px, transparent 50%);
  overflow: hidden;
  padding: 24px 16px;
}

/* Background Visual Layer */
.background-decorations {
  position: absolute;
  inset: 0;
  pointer-events: none;
  overflow: hidden;
  z-index: 0;
}

.grid-pattern {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(rgba(148, 163, 184, 0.25) 1px, transparent 1px);
  background-size: 28px 28px;
  mask-image: radial-gradient(ellipse at center, rgba(0,0,0,1) 30%, rgba(0,0,0,0) 80%);
  opacity: 0.6;
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.5;
}

.glow-orb-top-left {
  top: -100px;
  left: -100px;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(13, 148, 136, 0.15) 0%, rgba(204, 251, 241, 0) 70%);
}

.glow-orb-bottom-right {
  bottom: -120px;
  right: -120px;
  width: 550px;
  height: 550px;
  background: radial-gradient(circle, rgba(15, 23, 42, 0.12) 0%, rgba(241, 245, 249, 0) 70%);
}

/* Content Container */
.login-content {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 440px;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(18px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Main Card */
.login-card {
  width: 100%;
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid rgba(226, 232, 240, 0.9);
  box-shadow: 0 25px 50px -12px rgba(15, 23, 42, 0.09), 0 0 1px rgba(15, 23, 42, 0.08);
  overflow: hidden;
  position: relative;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-accent-bar {
  height: 4px;
  width: 100%;
  background: linear-gradient(90deg, #00b4d8 0%, #0d9488 50%, #0f172a 100%);
}

.card-body {
  padding: 38px 36px 32px 36px;
}

/* Header */
.card-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-bottom: 32px;
}

.brand-subtitle {
  font-family: var(--font-family);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.14em;
  color: #64748b;
  margin-top: 14px;
  text-transform: uppercase;
}

/* SSO Section */
.sso-section {
  margin-bottom: 20px;
}

.sso-button {
  width: 100%;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  background-color: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  padding: 0 20px;
  font-family: var(--font-family);
  font-size: 14.5px;
  font-weight: 500;
  color: #0f172a;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 2px 4px rgba(15, 23, 42, 0.03);
}

.sso-button:hover:not(:disabled) {
  background-color: #ffffff;
  border-color: #94a3b8;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px -4px rgba(15, 23, 42, 0.12), 0 2px 4px rgba(15, 23, 42, 0.04);
}

.sso-button:hover:not(:disabled) .button-arrow {
  transform: translateX(3px);
  color: #00b4d8;
}

.sso-button:active:not(:disabled) {
  transform: translateY(0) scale(0.99);
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08);
}

.sso-button:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.microsoft-icon-box {
  display: flex;
  align-items: center;
  justify-content: center;
}

.microsoft-icon {
  width: 19px;
  height: 19px;
}

.button-text {
  flex: 1;
  text-align: center;
}

.button-arrow {
  width: 18px;
  height: 18px;
  color: #64748b;
  transition: transform 0.2s ease, color 0.2s ease;
}

/* Trust Badge */
.sso-trust-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 12px;
  background-color: #f8fafc;
  border: 1px dashed #e2e8f0;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  color: #475569;
  margin-bottom: 24px;
}

.lock-shield-icon {
  width: 14px;
  height: 14px;
  color: #0d9488;
}

/* Card Footer */
.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 18px;
  border-top: 1px solid #f1f5f9;
}

.security-info {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #64748b;
}

.shield-check-icon {
  width: 15px;
  height: 15px;
  color: #0d9488;
}

.help-link {
  font-size: 12px;
  font-weight: 500;
  color: #0d9488;
  text-decoration: none;
  transition: color 0.15s ease;
}

.help-link:hover {
  color: #0f766e;
  text-decoration: underline;
}



/* Form Elements */
.login-form {
  width: 100%;
}

.input-group {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-group label {
  font-size: 13px;
  font-weight: 600;
  color: #475569;
}

.input-group input {
  height: 48px;
  padding: 0 16px;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  font-size: 14.5px;
  color: #0f172a;
  outline: none;
  transition: all 0.2s ease;
}

.input-group input:focus {
  border-color: #0d9488;
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.12);
}

.error-msg {
  color: #ef4444;
  font-size: 13px;
  margin-bottom: 16px;
  text-align: center;
}
.spinner-container {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #475569;
  font-size: 14px;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid #cbd5e1;
  border-top-color: #00b4d8;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .card-body {
    padding: 30px 24px 24px 24px;
  }
}
</style>
