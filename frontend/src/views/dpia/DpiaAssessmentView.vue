<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import PmSidebar from './components/PmSidebar.vue'

const router = useRouter()
const authStore = useAuthStore()
const searchQuery = ref('')
const currentStep = ref(1) // Step 1: Basic Details, Step 2: Screening Matrix, Step 3: Assign DPS

// Step 1 Form Fields
const projectName = ref('Global HRIS Migration')
const businessUnit = ref('hr')
const projectManager = ref('Executive Admin')
const goLiveDate = ref('2026-10-15')
const purposeOfProcessing = ref('Consolidate global employee records into a unified cloud database for HR analytics and payroll processing.')

// Interactive Data Category Tags
interface DataCategory {
  id: string
  label: string
  selected: boolean
}

const dataCategories = ref<DataCategory[]>([
  { id: 'personal_id', label: 'Personal ID', selected: true },
  { id: 'financial_data', label: 'Financial Data', selected: true },
  { id: 'health_info', label: 'Health Info', selected: true },
  { id: 'biometric', label: 'Biometric', selected: false },
  { id: 'location_data', label: 'Location Data', selected: false }
])

const toggleCategory = (category: DataCategory) => {
  category.selected = !category.selected
}

// Step 2: Screening Matrix Questions (Binary YES/NO Toggles)
const screening = ref({
  personalData: 'yes',
  sensitiveData: 'no',
  automatedDecision: 'yes',
  systematicMonitoring: 'no',
  largeScale: 'yes',
  crossBorder: 'no'
})

// Dynamic Real-time Risk Score Calculation
const riskScore = computed(() => {
  let score = 15
  if (screening.value.personalData === 'yes') score += 15
  if (screening.value.sensitiveData === 'yes') score += 20
  if (screening.value.automatedDecision === 'yes') score += 25
  if (screening.value.systematicMonitoring === 'yes') score += 15
  if (screening.value.largeScale === 'yes') score += 10
  if (screening.value.crossBorder === 'yes') score += 10
  return Math.min(100, score)
})

const isDpiaRequired = computed(() => riskScore.value >= 60)

const handleNavigateDashboard = () => {
  router.push('/pm/dashboard')
}

const handleNavigateAdmin = () => {
  router.push('/admin')
}

const handleNavigateModules = () => {
  router.push('/modules')
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const handleSaveDraft = () => {
  window.alert('DPIA Assessment Draft saved successfully!')
}

const handleNextStep = () => {
  if (currentStep.value < 3) {
    currentStep.value++
  } else {
    window.alert('DPIA Assessment submitted successfully for DPO Review!')
    router.push('/pm/dashboard')
  }
}

const handlePrevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}
</script>

<template>
  <div class="dpia-assessment-layout">
    <!-- Top Header Navigation Bar -->
    <header class="top-navbar">
      <!-- Left Logo Section -->
      <div class="navbar-brand" @click="handleNavigateModules" title="Back to Modules">
        <img src="/Aegislogo.jpeg" alt="Aegis360 Logo" class="brand-logo-img" />
      </div>

      <!-- Center Search Bar -->
      <div class="search-container">
        <div class="search-input-wrapper">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search ERP data..."
            class="search-input"
          />
        </div>
      </div>

      <!-- Right Action & Profile Section -->
      <div class="navbar-actions">
        <button type="button" class="notification-btn" title="Notifications">
          <svg class="bell-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
          </svg>
          <span class="notification-dot"></span>
        </button>

        <div class="user-profile-menu" @click="handleLogout" title="Click to Sign Out">
          <div class="user-info">
            <span class="user-name">{{ authStore.user.name }}</span>
            <span class="user-role">{{ authStore.user.role }}</span>
          </div>
          <div class="avatar-container">
            <img :src="authStore.user.avatar" :alt="authStore.user.name" class="user-avatar" />
          </div>
        </div>
      </div>
    </header>

    <!-- Main Container with Left Sidebar & Form Workspace -->
    <div class="body-container">
      <!-- Left Sidebar Navigation -->
      <PmSidebar />

      <!-- Main Dedicated Workspace Area -->
      <main class="main-content">
        <!-- ============================================ -->
        <!-- STEP 1: BASIC DETAILS                        -->
        <!-- ============================================ -->
        <div v-if="currentStep === 1">
          <!-- Page Header -->
          <header class="assessment-header">
            <div class="header-titles">
              <h1 class="page-title">New DPIA Assessment</h1>
              <p class="step-subtitle">Step 1 of 3: Core Project Information</p>
            </div>

            <div class="header-buttons">
              <button type="button" class="btn-save-draft" @click="handleSaveDraft">
                SAVE DRAFT
              </button>
              <button type="button" class="btn-next-step" @click="handleNextStep">
                <span>NEXT STEP</span>
                <svg class="next-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                  <polyline points="12 5 19 12 12 19"></polyline>
                </svg>
              </button>
            </div>
          </header>

          <!-- 3-Step Stepper Progress Bar -->
          <div class="stepper-container">
            <div class="stepper-track"></div>
            <div class="stepper-step active">
              <div class="step-circle">1</div>
              <span class="step-label">BASIC DETAILS</span>
            </div>
            <div class="stepper-step">
              <div class="step-circle">2</div>
              <span class="step-label">SCREENING</span>
            </div>
            <div class="stepper-step">
              <div class="step-circle">3</div>
              <span class="step-label">ASSIGN DPS</span>
            </div>
          </div>

          <!-- Form & Guidance Layout Grid -->
          <div class="assessment-card-container">
            <div class="assessment-grid">
              <div class="form-column">
                <div class="form-block">
                  <h2 class="block-title">General Information</h2>
                  <div class="block-divider"></div>

                  <div class="field-group">
                    <label class="field-label">PROJECT NAME <span class="required-star">*</span></label>
                    <input v-model="projectName" type="text" placeholder="e.g., Global HRIS Migration" class="field-input" />
                  </div>

                  <div class="field-grid-2">
                    <div class="field-group">
                      <label class="field-label">BUSINESS UNIT</label>
                      <select v-model="businessUnit" class="field-select">
                        <option value="" disabled>Select Business Unit...</option>
                        <option value="hr">Human Resources</option>
                        <option value="engineering">Core Engineering</option>
                        <option value="finance">Finance & Accounting</option>
                        <option value="operations">Global Operations</option>
                      </select>
                    </div>

                    <div class="field-group">
                      <label class="field-label">PROJECT MANAGER</label>
                      <div class="input-with-icon">
                        <svg class="field-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                          <circle cx="12" cy="7" r="4"></circle>
                        </svg>
                        <input v-model="projectManager" type="text" placeholder="Search employee directory..." class="field-input icon-padded" />
                      </div>
                    </div>
                  </div>

                  <div class="field-group max-w-sm">
                    <label class="field-label">ANTICIPATED GO-LIVE DATE</label>
                    <input v-model="goLiveDate" type="date" class="field-input" />
                  </div>
                </div>

                <div class="form-block">
                  <h2 class="block-title">Processing Scope</h2>
                  <div class="block-divider"></div>

                  <div class="field-group">
                    <label class="field-label">PURPOSE OF PROCESSING <span class="required-star">*</span></label>
                    <textarea v-model="purposeOfProcessing" rows="4" placeholder="Describe the specific goals and intended outcomes of this data processing activity..." class="field-textarea"></textarea>
                    <p class="field-caption"><span class="info-icon">ⓘ</span> Please be as detailed as possible to aid the screening phase.</p>
                  </div>

                  <div class="field-group">
                    <label class="field-label">DATA CATEGORIES INVOLVED</label>
                    <div class="category-tags-row">
                      <button v-for="cat in dataCategories" :key="cat.id" type="button" class="tag-pill" :class="{ selected: cat.selected }" @click="toggleCategory(cat)">
                        <span>{{ cat.label }}</span>
                        <span class="tag-action-icon">{{ cat.selected ? '×' : '+' }}</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <div class="guidance-column">
                <div class="guidance-card">
                  <div class="guidance-header">
                    <span class="question-icon">❓</span>
                    <h3 class="guidance-title">Guidance</h3>
                  </div>
                  <p class="guidance-text">
                    The Basic Details phase is crucial for establishing the preliminary risk profile of the project. Ensure the Purpose of Processing clearly articulates why the data is needed, not just how it will be used.
                  </p>
                  <div class="required-fields-box">
                    <h4 class="required-box-title">REQUIRED FIELDS</h4>
                    <ul class="required-list">
                      <li>• Project Name</li>
                      <li>• Purpose of Processing</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ============================================ -->
        <!-- STEP 2: SCREENING MATRIX (FIGMA SPECIFIED)   -->
        <!-- ============================================ -->
        <div v-else-if="currentStep === 2" class="screening-matrix-step">
          <!-- Module Meta & Header -->
          <header class="screening-header-row">
            <div class="meta-left">
              <span class="meta-tag">MODULE: DATA PROTECTION IMPACT ASSESSMENT • REF: DPIA-2023-084</span>
              <h1 class="page-title">Screening Matrix</h1>
            </div>

            <!-- Segmented Sub-Step Progress & Step Counter -->
            <div class="segmented-progress-box">
              <div class="segmented-bars">
                <span class="segment filled"></span>
                <span class="segment filled"></span>
                <span class="segment"></span>
                <span class="segment"></span>
              </div>
              <span class="step-count-label">Step 2 of 4</span>
            </div>
          </header>

          <!-- 2-Column Screening Workspace -->
          <div class="screening-grid">
            <!-- Left Column: Modular Question Cards -->
            <div class="screening-questions-col">
              <!-- Block 1: Data Processing Scope -->
              <div class="matrix-card">
                <div class="matrix-card-header">
                  <div class="card-title-group">
                    <svg class="matrix-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <ellipse cx="12" cy="5" rx="9" ry="3"></ellipse>
                      <path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"></path>
                      <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"></path>
                    </svg>
                    <div>
                      <h2 class="matrix-card-title">Data Processing Scope</h2>
                      <p class="matrix-card-subtitle">Determine the fundamental nature of the data involved in this project phase.</p>
                    </div>
                  </div>
                  <span class="mandatory-badge">● MANDATORY</span>
                </div>

                <div class="question-item-box">
                  <div class="question-info">
                    <h3 class="question-text">Is personal data processed?</h3>
                    <p class="question-subtext">Includes names, IP addresses, location data, or any identifiers.</p>
                  </div>
                  <div class="toggle-group">
                    <button type="button" class="btn-toggle" :class="{ active: screening.personalData === 'yes' }" @click="screening.personalData = 'yes'">YES</button>
                    <button type="button" class="btn-toggle dark-active" :class="{ active: screening.personalData === 'no' }" @click="screening.personalData = 'no'">NO</button>
                  </div>
                </div>

                <div class="question-item-box">
                  <div class="question-info">
                    <h3 class="question-text">Is sensitive data involved?</h3>
                    <p class="question-subtext">Special categories under GDPR (e.g., health, biometrics, political opinions).</p>
                  </div>
                  <div class="toggle-group">
                    <button type="button" class="btn-toggle" :class="{ active: screening.sensitiveData === 'yes' }" @click="screening.sensitiveData = 'yes'">YES</button>
                    <button type="button" class="btn-toggle dark-active" :class="{ active: screening.sensitiveData === 'no' }" @click="screening.sensitiveData = 'no'">NO</button>
                  </div>
                </div>
              </div>

              <!-- Block 2: Algorithmic Impact -->
              <div class="matrix-card">
                <div class="matrix-card-header">
                  <div class="card-title-group">
                    <svg class="matrix-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                    </svg>
                    <div>
                      <h2 class="matrix-card-title">Algorithmic Impact</h2>
                      <p class="matrix-card-subtitle">Evaluate the use of automated systems and profiling mechanisms.</p>
                    </div>
                  </div>
                </div>

                <div class="question-item-box">
                  <div class="question-info">
                    <h3 class="question-text">Automated decision making? <span class="alert-inline-icon">⚠️</span></h3>
                    <p class="question-subtext">Decisions made without human involvement that have legal effects.</p>
                  </div>
                  <div class="toggle-group">
                    <button type="button" class="btn-toggle alert-red" :class="{ active: screening.automatedDecision === 'yes' }" @click="screening.automatedDecision = 'yes'">YES</button>
                    <button type="button" class="btn-toggle dark-active" :class="{ active: screening.automatedDecision === 'no' }" @click="screening.automatedDecision = 'no'">NO</button>
                  </div>
                </div>

                <div class="question-item-box">
                  <div class="question-info">
                    <h3 class="question-text">Systematic monitoring?</h3>
                    <p class="question-subtext">Large scale monitoring of publicly accessible areas.</p>
                  </div>
                  <div class="toggle-group">
                    <button type="button" class="btn-toggle" :class="{ active: screening.systematicMonitoring === 'yes' }" @click="screening.systematicMonitoring = 'yes'">YES</button>
                    <button type="button" class="btn-toggle dark-active" :class="{ active: screening.systematicMonitoring === 'no' }" @click="screening.systematicMonitoring = 'no'">NO</button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Right Column: Real-Time Live Assessment Widget & Action Buttons -->
            <div class="screening-sidebar-col">
              <!-- Dark Navy Live Assessment Card -->
              <div class="live-assessment-card">
                <div class="live-card-header">
                  <svg class="chart-header-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="18" height="18" rx="2"></rect>
                    <line x1="9" y1="9" x2="9" y2="15"></line>
                    <line x1="15" y1="15" x2="15" y2="11"></line>
                  </svg>
                  <span>Live Assessment</span>
                </div>

                <!-- Circular Risk Arc Gauge -->
                <div class="risk-gauge-container">
                  <svg class="gauge-svg" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="38" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="6" />
                    <circle
                      cx="50"
                      cy="50"
                      r="38"
                      fill="none"
                      :stroke="isDpiaRequired ? '#ef4444' : '#10b981'"
                      stroke-width="7"
                      stroke-dasharray="238.7"
                      :stroke-dashoffset="238.7 - (238.7 * riskScore) / 100"
                      stroke-linecap="round"
                      transform="rotate(-90 50 50)"
                    />
                  </svg>
                  <div class="gauge-center-text">
                    <span class="score-val">{{ riskScore }}</span>
                    <span class="score-lbl">RISK SCORE</span>
                  </div>
                </div>

                <!-- Status Alert Box inside Card -->
                <div class="status-alert-box" :class="{ 'dpia-required': isDpiaRequired }">
                  <div class="alert-title-row">
                    <span class="alert-mark">!</span>
                    <span class="alert-heading">STATUS</span>
                  </div>
                  <h4 class="status-main-label">{{ isDpiaRequired ? 'DPIA REQUIRED' : 'STANDARD SCREENING' }}</h4>
                  <p class="status-sub-desc">
                    {{ isDpiaRequired ? 'Automated decision making triggers mandatory assessment under Article 35(3)(a).' : 'Standard risk profile within normal operational limits.' }}
                  </p>
                </div>

                <div class="gauge-summary-metrics">
                  <div class="metric-row">
                    <span class="m-label">Threshold crossed</span>
                    <span class="m-value" :class="{ highlight: isDpiaRequired }">{{ isDpiaRequired ? 'YES' : 'NO' }}</span>
                  </div>
                  <div class="metric-row">
                    <span class="m-label">Consultation needed</span>
                    <span class="m-value dpo-highlight">{{ isDpiaRequired ? 'DPO' : 'None' }}</span>
                  </div>
                </div>
              </div>

              <!-- Action Buttons Stack -->
              <div class="screening-actions-stack">
                <button type="button" class="btn-sidebar-draft" @click="handleSaveDraft">
                  Save Draft
                </button>
                <button type="button" class="btn-sidebar-next" @click="handleNextStep">
                  <span>Next Step</span>
                  <svg class="next-icn" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                    <polyline points="12 5 19 12 12 19"></polyline>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- ============================================ -->
        <!-- STEP 3: ASSIGN DPS / SUBMISSION              -->
        <!-- ============================================ -->
        <div v-else-if="currentStep === 3" class="step3-workspace">
          <header class="assessment-header">
            <div class="header-titles">
              <h1 class="page-title">Assign DPO Reviewer</h1>
              <p class="step-subtitle">Step 3 of 3: Finalize Assessment & Submit</p>
            </div>
            <div class="header-buttons">
              <button type="button" class="btn-save-draft" @click="handlePrevStep">BACK</button>
              <button type="button" class="btn-next-step" @click="handleNextStep">SUBMIT FOR DPO REVIEW →</button>
            </div>
          </header>

          <div class="assessment-card-container">
            <div class="dpo-assign-box">
              <h2 class="block-title">Select Data Protection Officer (DPO)</h2>
              <p class="guidance-text" style="margin-bottom: 20px;">
                Based on your high risk score of <strong>{{ riskScore }}</strong>, mandatory DPO consultation is required under GDPR Article 35.
              </p>
              
              <div class="field-group max-w-sm">
                <label class="field-label">ASSIGNED REVIEWS DPO</label>
                <select class="field-select">
                  <option selected>Marcus Vance (Head DPO - Global Compliance)</option>
                  <option>Elena Rostova (Senior Privacy Counsel)</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
.dpia-assessment-layout {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f8fafc;
}

/* Top Navbar */
.top-navbar {
  height: 105px;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-brand {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.brand-logo-img {
  height: 90px;
  width: auto;
  object-fit: contain;
}

.search-container {
  flex: 1;
  max-width: 480px;
  margin: 0 40px;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 16px;
  width: 18px;
  height: 18px;
  color: #94a3b8;
}

.search-input {
  width: 100%;
  height: 44px;
  padding: 0 18px 0 46px;
  background-color: #f1f5f9;
  border: 1px solid transparent;
  border-radius: 10px;
  font-family: var(--font-family);
  font-size: 14px;
  color: #0f172a;
  outline: none;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 24px;
}

.notification-btn {
  position: relative;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  cursor: pointer;
  width: 42px;
  height: 42px;
  color: #475569;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bell-icon {
  width: 20px;
  height: 20px;
}

.notification-dot {
  position: absolute;
  top: 9px;
  right: 9px;
  width: 8px;
  height: 8px;
  background-color: #ef4444;
  border: 2px solid #ffffff;
  border-radius: 50%;
}

.user-profile-menu {
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 12px;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.user-name {
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
}

.user-role {
  font-size: 11.5px;
  color: #64748b;
  margin-top: 2px;
}

.avatar-container {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #e2e8f0;
}

.user-avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Body Container */
.body-container {
  flex: 1;
  display: flex;
}

/* Main Workspace */
.main-content {
  flex: 1;
  padding: 36px 48px;
  background-color: #f8fafc;
  overflow-y: auto;
}

/* Assessment Step 1 Header */
.assessment-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 28px;
}

.page-title {
  font-family: var(--font-family);
  font-size: 30px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.02em;
}

.step-subtitle {
  font-size: 14px;
  color: #64748b;
  margin-top: 4px;
}

.header-buttons {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn-save-draft {
  height: 42px;
  padding: 0 20px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-family: var(--font-family);
  font-size: 12.5px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: #334155;
  cursor: pointer;
}

.btn-next-step {
  height: 42px;
  padding: 0 22px;
  background: #0f2942;
  border: none;
  border-radius: 8px;
  font-family: var(--font-family);
  font-size: 12.5px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: #ffffff;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.next-arrow {
  width: 15px;
  height: 15px;
}

/* Stepper Bar */
.stepper-container {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 36px;
  padding: 0 10%;
}

.stepper-track {
  position: absolute;
  top: 18px;
  left: 12%;
  right: 12%;
  height: 2px;
  background-color: #e2e8f0;
  z-index: 1;
}

.stepper-step {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.step-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #e2e8f0;
  color: #64748b;
  font-size: 14px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stepper-step.active .step-circle {
  background-color: #0f2942;
  color: #ffffff;
  box-shadow: 0 0 0 4px rgba(15, 41, 66, 0.15);
}

.step-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #94a3b8;
}

.stepper-step.active .step-label {
  color: #0f2942;
}

/* Form Container */
.assessment-card-container {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 36px;
  box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
}

.assessment-grid {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 40px;
}

.form-column {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.form-block {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.block-title {
  font-family: var(--font-family);
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
}

.block-divider {
  height: 1px;
  background-color: #e2e8f0;
  margin-top: -6px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.max-w-sm {
  max-width: 320px;
}

.field-label {
  font-size: 11.5px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #475569;
}

.required-star {
  color: #ef4444;
}

.field-input, .field-select, .field-textarea {
  width: 100%;
  padding: 0 16px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-family: var(--font-family);
  font-size: 14px;
  color: #0f172a;
  outline: none;
}

.field-input {
  height: 44px;
}

.field-select {
  height: 44px;
  cursor: pointer;
}

.field-textarea {
  padding: 14px 16px;
}

.field-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.field-icon {
  position: absolute;
  left: 14px;
  width: 16px;
  height: 16px;
  color: #94a3b8;
}

.icon-padded {
  padding-left: 40px;
}

.field-caption {
  font-size: 12px;
  color: #64748b;
  display: flex;
  align-items: center;
  gap: 6px;
}

.category-tags-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tag-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 9999px;
  font-family: var(--font-family);
  font-size: 13px;
  font-weight: 500;
  color: #334155;
  cursor: pointer;
}

.tag-pill.selected {
  background: #ccfbf1;
  border-color: #0d9488;
  color: #0f766e;
  font-weight: 600;
}

.guidance-column {
  border-left: 1px solid #f1f5f9;
  padding-left: 32px;
}

.guidance-card {
  background: #f0fdfa;
  border: 1px solid #ccfbf1;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.guidance-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.guidance-title {
  font-family: var(--font-family);
  font-size: 15px;
  font-weight: 700;
  color: #0f766e;
}

.guidance-text {
  font-size: 12.5px;
  color: #334155;
  line-height: 1.5;
}

.required-fields-box {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 12px 14px;
}

.required-box-title {
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #64748b;
  margin-bottom: 6px;
}

.required-list {
  list-style: none;
  font-size: 12px;
  color: #334155;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

/* ============================================ */
/* STEP 2: SCREENING MATRIX STYLING (FIGMA MATCH) */
/* ============================================ */
.screening-matrix-step {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.screening-header-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
}

.meta-tag {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #64748b;
  display: block;
  margin-bottom: 4px;
}

.segmented-progress-box {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
}

.segmented-bars {
  display: flex;
  gap: 6px;
}

.segment {
  width: 32px;
  height: 5px;
  background-color: #e2e8f0;
  border-radius: 4px;
}

.segment.filled {
  background-color: #0f2942;
}

.step-count-label {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
}

.screening-grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 28px;
}

.screening-questions-col {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.matrix-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 28px;
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.03);
}

.matrix-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 24px;
}

.card-title-group {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.matrix-icon {
  width: 22px;
  height: 22px;
  color: #0d9488;
  margin-top: 2px;
}

.matrix-card-title {
  font-family: var(--font-family);
  font-size: 19px;
  font-weight: 700;
  color: #0f172a;
}

.matrix-card-subtitle {
  font-size: 13px;
  color: #64748b;
  margin-top: 2px;
}

.mandatory-badge {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #334155;
  background: #f1f5f9;
  padding: 4px 10px;
  border-radius: 6px;
}

.question-item-box {
  background: #f8fafc;
  border-radius: 12px;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 16px;
}

.question-item-box:last-child {
  margin-bottom: 0;
}

.question-text {
  font-size: 14.5px;
  font-weight: 700;
  color: #0f172a;
}

.question-subtext {
  font-size: 12.5px;
  color: #64748b;
  margin-top: 2px;
}

.alert-inline-icon {
  font-size: 13px;
}

.toggle-group {
  display: flex;
  gap: 6px;
  background: #e2e8f0;
  padding: 3px;
  border-radius: 8px;
}

.btn-toggle {
  height: 36px;
  padding: 0 22px;
  border-radius: 6px;
  border: none;
  background: transparent;
  font-family: var(--font-family);
  font-size: 13px;
  font-weight: 700;
  color: #475569;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-toggle.active {
  background: #ffffff;
  color: #0f172a;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08);
}

.btn-toggle.dark-active.active {
  background: #0f2942;
  color: #ffffff;
}

.btn-toggle.alert-red.active {
  background: #dc2626;
  color: #ffffff;
}

/* Screening Right Column (Live Assessment Widget) */
.screening-sidebar-col {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.live-assessment-card {
  background: #0a1324;
  border-radius: 16px;
  padding: 24px;
  color: #ffffff;
  box-shadow: 0 10px 30px rgba(10, 19, 36, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.live-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  font-size: 15px;
  font-weight: 700;
  color: #94a3b8;
}

.chart-header-icon {
  width: 18px;
  height: 18px;
}

.risk-gauge-container {
  position: relative;
  width: 140px;
  height: 140px;
  margin: 20px 0;
}

.gauge-svg {
  width: 100%;
  height: 100%;
}

.gauge-center-text {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.score-val {
  font-family: var(--font-family);
  font-size: 34px;
  font-weight: 800;
  color: #ffffff;
  line-height: 1;
}

.score-lbl {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #94a3b8;
  margin-top: 2px;
}

.status-alert-box {
  width: 100%;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 12px;
  padding: 16px;
  color: #991b1b;
  margin-bottom: 20px;
}

.alert-title-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.06em;
}

.alert-mark {
  width: 14px;
  height: 14px;
  background: #dc2626;
  color: #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 900;
}

.status-main-label {
  font-family: var(--font-family);
  font-size: 16px;
  font-weight: 800;
  color: #991b1b;
  margin-top: 4px;
}

.status-sub-desc {
  font-size: 11.5px;
  color: #7f1d1d;
  line-height: 1.4;
  margin-top: 4px;
}

.gauge-summary-metrics {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
  border-top: 1px solid rgba(255,255,255,0.1);
  padding-top: 14px;
}

.metric-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
}

.m-label {
  color: #94a3b8;
}

.m-value {
  font-weight: 700;
  color: #ffffff;
}

.m-value.highlight {
  color: #ef4444;
}

.dpo-highlight {
  color: #ef4444;
}

.screening-actions-stack {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.btn-sidebar-draft {
  width: 100%;
  height: 44px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  font-family: var(--font-family);
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  cursor: pointer;
}

.btn-sidebar-next {
  width: 100%;
  height: 48px;
  background: #030712;
  border: none;
  border-radius: 10px;
  font-family: var(--font-family);
  font-size: 14.5px;
  font-weight: 600;
  color: #ffffff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.next-icn {
  width: 16px;
  height: 16px;
}

@media (max-width: 1024px) {
  .screening-grid {
    grid-template-columns: 1fr;
  }
}
</style>
