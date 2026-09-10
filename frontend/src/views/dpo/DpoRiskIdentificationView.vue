<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import DpoSidebar from './components/DpoSidebar.vue'
import { dpiaApi, type AssessmentSummary } from '@/services/api'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const assessmentId = computed(() => route.params.id as string)
const assessment = ref<AssessmentSummary | null>(null)
const isLoading = ref(true)

// Mock risks array
const identifiedRisks = ref<any[]>([])

// Form state
const currentRisk = ref({
  title: '',
  description: '',
  impact: '',
  likelihood: '',
  mitigation: ''
})

const severities = ['Low', 'Medium', 'High', 'Critical']

const loadData = async () => {
  isLoading.value = true
  try {
    const res = await dpiaApi.getAssessment(assessmentId.value)
    assessment.value = res.assessment
  } catch (err) {
    console.error('Failed to load assessment', err)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadData()
})

const selectImpact = (level: string) => {
  currentRisk.value.impact = level
}

const selectLikelihood = (level: string) => {
  currentRisk.value.likelihood = level
}

const addRisk = () => {
  if (!currentRisk.value.title || !currentRisk.value.impact || !currentRisk.value.likelihood) {
    alert('Please fill in the title, impact, and likelihood before adding the risk.')
    return
  }

  identifiedRisks.value.push({
    id: `RSK-${Math.floor(Math.random() * 10000)}`,
    ...currentRisk.value
  })

  // Reset form
  currentRisk.value = {
    title: '',
    description: '',
    impact: '',
    likelihood: '',
    mitigation: ''
  }
}

const removeRisk = (index: number) => {
  identifiedRisks.value.splice(index, 1)
}

const finalizeAssessment = () => {
  // In a real app, this would save the risks to the backend via dpiaApi
  alert(`Successfully saved ${identifiedRisks.value.length} risks to the assessment. Returning to Dashboard.`)
  router.push('/dpo/dashboard')
}

// Styling helpers
const getSeverityClass = (severity: string) => {
  switch (severity) {
    case 'Critical': return 'badge-critical'
    case 'High': return 'badge-high'
    case 'Medium': return 'badge-medium'
    case 'Low': return 'badge-low'
    default: return 'badge-low'
  }
}
</script>

<template>
  <div class="dashboard-layout">
    <DpoSidebar />

    <main class="main-content">
      <header class="top-nav">
        <div class="nav-left">
          <button class="btn-back-nav" @click="router.push('/dpo/dashboard')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
            Dashboard
          </button>
        </div>
        <div class="nav-actions">
          <div class="user-profile">
            <div class="user-info">
              <span class="user-name">{{ authStore.user.name }}</span>
              <span class="user-role">{{ authStore.user.role }}</span>
            </div>
            <img :src="authStore.user.avatar" alt="Profile" class="avatar" />
          </div>
        </div>
      </header>

      <div class="content-scroll-area">
        <div class="page-header">
          <div class="header-titles">
            <span class="step-label">POST-PIA PHASE</span>
            <h1 class="page-title">Risk Identification & Mitigation</h1>
            <p class="page-subtitle" v-if="assessment">
              Identify risks for: <strong>{{ assessment.title }}</strong>
            </p>
          </div>
        </div>

        <div class="risk-layout">
          <!-- Left Column: Risk Entry Form -->
          <div class="risk-form-container">
            <div class="card-glass">
              <h3 class="form-title">Add New Risk</h3>
              
              <div class="form-group">
                <label>Risk Title</label>
                <input 
                  type="text" 
                  v-model="currentRisk.title" 
                  placeholder="e.g. Unauthorized access to sensitive data"
                  class="form-input"
                />
              </div>

              <div class="form-group">
                <label>Detailed Description</label>
                <textarea 
                  v-model="currentRisk.description"
                  placeholder="Describe the risk scenario, vulnerabilities, and potential consequences..."
                  class="form-input textarea-tall"
                ></textarea>
              </div>

              <div class="grid-2-col">
                <div class="form-group">
                  <label>Impact Level</label>
                  <div class="pill-group">
                    <button 
                      v-for="sev in severities" 
                      :key="'imp-'+sev"
                      type="button"
                      class="pill-btn"
                      :class="[{ 'active': currentRisk.impact === sev }, `pill-${sev.toLowerCase()}`]"
                      @click="selectImpact(sev)"
                    >
                      {{ sev }}
                    </button>
                  </div>
                </div>

                <div class="form-group">
                  <label>Likelihood</label>
                  <div class="pill-group">
                    <button 
                      v-for="sev in severities" 
                      :key="'lik-'+sev"
                      type="button"
                      class="pill-btn"
                      :class="[{ 'active': currentRisk.likelihood === sev }, `pill-${sev.toLowerCase()}`]"
                      @click="selectLikelihood(sev)"
                    >
                      {{ sev }}
                    </button>
                  </div>
                </div>
              </div>

              <div class="form-group">
                <label>Proposed Mitigation Plan</label>
                <textarea 
                  v-model="currentRisk.mitigation"
                  placeholder="What controls or actions will reduce the likelihood or impact?"
                  class="form-input"
                ></textarea>
              </div>

              <div class="form-actions">
                <button class="btn-primary" @click="addRisk">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="12" y1="5" x2="12" y2="19"></line>
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                  </svg>
                  Add Risk to Register
                </button>
              </div>
            </div>
          </div>

          <!-- Right Column: Risk Inventory -->
          <div class="risk-inventory-container">
            <div class="inventory-header">
              <h3>Identified Risks ({{ identifiedRisks.length }})</h3>
            </div>
            
            <div class="inventory-list">
              <div v-if="identifiedRisks.length === 0" class="empty-state">
                <div class="empty-icon">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                  </svg>
                </div>
                <p>No risks identified yet.</p>
                <span>Add risks using the form to build your register.</span>
              </div>

              <div v-for="(risk, idx) in identifiedRisks" :key="risk.id" class="risk-card">
                <div class="risk-card-top">
                  <span class="risk-id">{{ risk.id }}</span>
                  <button class="btn-remove" @click="removeRisk(idx)" title="Remove Risk">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <line x1="18" y1="6" x2="6" y2="18"></line>
                      <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                  </button>
                </div>
                
                <h4 class="risk-title-disp">{{ risk.title }}</h4>
                
                <div class="risk-badges">
                  <div class="badge-col">
                    <span class="badge-label">Impact</span>
                    <span class="severity-badge" :class="getSeverityClass(risk.impact)">{{ risk.impact }}</span>
                  </div>
                  <div class="badge-col">
                    <span class="badge-label">Likelihood</span>
                    <span class="severity-badge" :class="getSeverityClass(risk.likelihood)">{{ risk.likelihood }}</span>
                  </div>
                </div>

                <div class="risk-mitigation-disp" v-if="risk.mitigation">
                  <strong>Mitigation:</strong>
                  <p>{{ risk.mitigation }}</p>
                </div>
              </div>
            </div>

            <div class="finalize-section">
              <button class="btn-success-lg" @click="finalizeAssessment" :disabled="identifiedRisks.length === 0">
                Finalize Assessment
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M5 12h14"></path>
                  <path d="M12 5l7 7-7 7"></path>
                </svg>
              </button>
            </div>
          </div>

        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.dashboard-layout {
  display: flex;
  height: 100vh;
  background-color: #f8fafc;
  font-family: 'Inter', system-ui, sans-serif;
  color: #1e293b;
  overflow: hidden;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Top Navigation */
.top-nav {
  height: 72px;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  flex-shrink: 0;
  z-index: 10;
}

.btn-back-nav {
  display: flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  border: none;
  color: #64748b;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  padding: 8px 0;
  transition: color 0.2s;
}

.btn-back-nav:hover {
  color: #0f172a;
}

.btn-back-nav svg {
  width: 18px;
  height: 18px;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
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
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #e2e8f0;
}

/* Content Area */
.content-scroll-area {
  padding: 40px;
  overflow-y: auto;
  flex: 1;
}

.page-header {
  margin-bottom: 32px;
}

.step-label {
  display: inline-block;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.1em;
  color: #F58425;
  background: #fff7ed;
  padding: 4px 10px;
  border-radius: 6px;
  margin-bottom: 12px;
}

.page-title {
  font-size: 32px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.02em;
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 15px;
  color: #64748b;
  margin: 0;
}
.page-subtitle strong {
  color: #0f172a;
}

/* Risk Layout */
.risk-layout {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 32px;
  align-items: start;
}

/* Glass Form Card */
.card-glass {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04);
  border-radius: 20px;
  padding: 32px;
}

.form-title {
  font-size: 20px;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 24px 0;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 700;
  color: #334155;
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  font-size: 14px;
  color: #0f172a;
  transition: all 0.2s;
  font-family: inherit;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #F58425;
  box-shadow: 0 0 0 3px rgba(245, 132, 37, 0.1);
}

textarea.form-input {
  min-height: 100px;
  resize: vertical;
}

.textarea-tall {
  min-height: 140px;
}

.grid-2-col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

/* Pill Buttons */
.pill-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.pill-btn {
  flex: 1;
  padding: 10px 0;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.pill-btn:hover {
  background: #e2e8f0;
}

/* Active States */
.pill-low.active {
  background: #f1f5f9;
  border-color: #94a3b8;
  color: #0f172a;
}
.pill-medium.active {
  background: #fef3c7;
  border-color: #fbbf24;
  color: #b45309;
}
.pill-high.active {
  background: #fee2e2;
  border-color: #f87171;
  color: #b91c1c;
}
.pill-critical.active {
  background: #fef2f2;
  border-color: #ef4444;
  color: #dc2626;
  font-weight: 800;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 32px;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #F58425;
  color: #ffffff;
  border: none;
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(245, 132, 37, 0.2);
  transition: all 0.2s;
}

.btn-primary:hover {
  background: #e0721c;
  transform: translateY(-2px);
}

.btn-primary svg {
  width: 18px;
  height: 18px;
}

/* Risk Inventory */
.risk-inventory-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.inventory-header h3 {
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
}

.inventory-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-height: 600px;
  overflow-y: auto;
  padding-right: 8px;
}

.empty-state {
  background: #ffffff;
  border: 2px dashed #cbd5e1;
  border-radius: 16px;
  padding: 40px 24px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.empty-icon {
  width: 48px;
  height: 48px;
  background: #f1f5f9;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  color: #94a3b8;
}
.empty-icon svg {
  width: 24px;
  height: 24px;
}

.empty-state p {
  font-size: 16px;
  font-weight: 700;
  color: #334155;
  margin: 0 0 8px 0;
}
.empty-state span {
  font-size: 13px;
  color: #64748b;
}

/* Risk Card */
.risk-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.02);
  transition: all 0.2s;
}

.risk-card:hover {
  border-color: #cbd5e1;
  box-shadow: 0 8px 24px rgba(0,0,0,0.05);
}

.risk-card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.risk-id {
  font-size: 12px;
  font-weight: 700;
  color: #94a3b8;
  letter-spacing: 0.05em;
}

.btn-remove {
  background: transparent;
  border: none;
  color: #cbd5e1;
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  transition: all 0.2s;
}
.btn-remove:hover {
  background: #fef2f2;
  color: #ef4444;
}
.btn-remove svg {
  width: 16px;
  height: 16px;
}

.risk-title-disp {
  font-size: 16px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 16px 0;
  line-height: 1.4;
}

.risk-badges {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f1f5f9;
}

.badge-col {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.badge-label {
  font-size: 11px;
  font-weight: 600;
  color: #94a3b8;
  text-transform: uppercase;
}

.severity-badge {
  font-size: 12px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
  display: inline-block;
}

.badge-critical {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}
.badge-high {
  background: #fff5f5;
  color: #c53030;
}
.badge-medium {
  background: #fffbeb;
  color: #b45309;
}
.badge-low {
  background: #f8fafc;
  color: #475569;
}

.risk-mitigation-disp {
  font-size: 13px;
  color: #475569;
  background: #f8fafc;
  padding: 12px;
  border-radius: 8px;
}
.risk-mitigation-disp strong {
  display: block;
  font-size: 12px;
  color: #0f172a;
  margin-bottom: 4px;
}
.risk-mitigation-disp p {
  margin: 0;
  line-height: 1.5;
}

/* Finalize Action */
.finalize-section {
  margin-top: 12px;
  padding-top: 24px;
  border-top: 2px dashed #e2e8f0;
}

.btn-success-lg {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  background: #0f172a;
  color: #ffffff;
  border: none;
  padding: 16px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-success-lg:hover:not(:disabled) {
  background: #1e293b;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.15);
}

.btn-success-lg:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
  opacity: 0.7;
}

.btn-success-lg svg {
  width: 20px;
  height: 20px;
}

/* Scrollbar styling for inventory list */
.inventory-list::-webkit-scrollbar {
  width: 6px;
}
.inventory-list::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}
.inventory-list::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 4px;
}
</style>
