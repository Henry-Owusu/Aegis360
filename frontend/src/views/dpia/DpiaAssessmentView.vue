<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import PmSidebar from './components/PmSidebar.vue'
import { dpiaApi } from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const currentStep = ref(1) // 1: Basic Data, 2: Screening, 3: Full PIA
const assessmentId = ref<string | null>(null)

// Step 1: Fixed metadata
const title = ref('')
const projectManager = ref('')

// Dynamic data
const basicDataQuestions = ref<any[]>([])
const screeningQuestions = ref<any[]>([])

// Responses dicts
const basicDataResponses = ref<Record<string, any>>({})
const screeningResponses = ref<Record<string, any>>({})

const isLoading = ref(false)

const loadQuestions = async () => {
  try {
    const [bd, sc] = await Promise.all([
      dpiaApi.getQuestions('basic_data'),
      dpiaApi.getQuestions('screening'),
    ])
    basicDataQuestions.value = bd.questions || []
    screeningQuestions.value = sc.questions || []
  } catch (error) {
    console.error('Failed to load questions', error)
  }
}

onMounted(() => {
  loadQuestions()
})

const handleNavigateModules = () => {
  router.push('/modules')
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const handleSaveDraft = async () => {
  if (currentStep.value === 1 && !assessmentId.value) {
    if (!title.value || !projectManager.value) {
      alert('Title and Project Manager are required to create a draft.')
      return
    }
    const res = await dpiaApi.createAssessment({
      title: title.value,
      project_manager: projectManager.value,
    })
    assessmentId.value = res.id
  }

  if (assessmentId.value) {
    if (currentStep.value === 1)
      await dpiaApi.saveResponses(assessmentId.value, basicDataResponses.value)
    if (currentStep.value === 2)
      await dpiaApi.saveResponses(assessmentId.value, screeningResponses.value)
  }
  window.alert('DPIA Assessment Draft saved successfully!')
}

const handleNextStep = async () => {
  isLoading.value = true
  try {
    if (currentStep.value === 1) {
      if (!assessmentId.value) {
        if (!title.value || !projectManager.value) {
          alert('Title and Project Manager are required to proceed.')
          isLoading.value = false
          return
        }
        const res = await dpiaApi.createAssessment({
          title: title.value,
          project_manager: projectManager.value,
        })
        assessmentId.value = res.id
      }
      await dpiaApi.saveResponses(assessmentId.value, basicDataResponses.value)
      currentStep.value = 2
    } else if (currentStep.value === 2) {
      await dpiaApi.saveResponses(assessmentId.value, screeningResponses.value)
      window.alert('DPIA Assessment submitted successfully for DPO Review!')
      router.push('/pm/dashboard')
    }
  } catch (err) {
    console.error('Error during step transition:', err)
    window.alert('Failed to save assessment. Please try again.')
  }
  isLoading.value = false
}

const handlePrevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

const renderInput = (question: any, vModelTarget: Record<string, any>) => {
  if (vModelTarget[question.id] === undefined) {
    if (question.answer_type === 'Checkbox' || question.answer_type === 'multi_choice') {
      vModelTarget[question.id] = []
    } else if (question.answer_type === 'matrix') {
      const initObj: any = {}
      if (question.options && question.options.rows) {
        question.options.rows.forEach((r: string) => {
          initObj[r] = []
        })
      }
      vModelTarget[question.id] = initObj
    } else {
      vModelTarget[question.id] = ''
    }
  }
  return ''
}
</script>

<template>
  <div class="dpia-assessment-layout">
    <header class="top-navbar">
      <div class="navbar-brand" @click="handleNavigateModules" title="Back to Modules">
        <img src="/Aegislogo.jpeg" alt="Aegis360 Logo" class="brand-logo-img" />
      </div>

      <div class="navbar-actions">
        <div class="user-profile-menu" @click="handleLogout" title="Click to Sign Out">
          <div class="user-info">
            <span class="user-name">{{ authStore.user?.name || 'Project Manager' }}</span>
            <span class="user-role">{{ authStore.primaryRole }}</span>
          </div>
          <div class="avatar-container">
            <img
              :src="authStore.user?.avatar || 'https://i.pravatar.cc/150?u=pm'"
              :alt="authStore.user?.name || 'User'"
              class="user-avatar"
            />
          </div>
        </div>
      </div>
    </header>

    <div class="main-body">
      <PmSidebar active-item="active-dpia" />

      <main class="content-area">
        <div class="wizard-header">
          <div class="wizard-title-block">
            <h1>Create DPIA Assessment</h1>
            <p>Complete the required sections below. Progress is saved automatically.</p>
          </div>
          <div class="wizard-actions">
            <button class="btn-secondary" @click="handleSaveDraft" :disabled="isLoading">
              Save Draft
            </button>
          </div>
        </div>

        <!-- Sleek Wizard Progress Bar -->
        <div class="wizard-progress-container">
          <div class="progress-track">
            <div
              class="progress-fill"
              :style="{ width: ((currentStep - 1) / 1) * 100 + '%' }"
            ></div>
          </div>
          <div class="progress-steps">
            <div :class="['step-node', { active: currentStep >= 1, completed: currentStep > 1 }]">
              <div class="step-circle">
                <svg
                  v-if="currentStep > 1"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="3"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                <span v-else>1</span>
              </div>
              <span class="step-label">Basic Data</span>
            </div>

            <div :class="['step-node', { active: currentStep >= 2 }]">
              <div class="step-circle">
                <span v-if="currentStep <= 2">2</span>
                <svg
                  v-else
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="3"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
              </div>
              <span class="step-label">Screening Matrix</span>
            </div>
          </div>
        </div>

        <div class="wizard-content card-glass">
          <!-- Step 1: Basic Data -->
          <div v-if="currentStep === 1" class="form-section fade-in">
            <h2 class="section-title">Core Properties</h2>

            <div class="form-grid">
              <div class="input-group full-width">
                <label>Assessment Title <span class="required">*</span></label>
                <input
                  type="text"
                  v-model="title"
                  class="form-input"
                  placeholder="Enter project or assessment name"
                />
              </div>

              <div class="input-group">
                <label>Project Manager <span class="required">*</span></label>
                <input
                  type="text"
                  v-model="projectManager"
                  class="form-input"
                  placeholder="Name of Project Manager"
                />
              </div>
            </div>

            <div v-if="basicDataQuestions.length > 0" class="divider"></div>

            <h2 class="section-title" v-if="basicDataQuestions.length > 0">Additional Details</h2>
            <div class="form-grid">
              <div v-for="q in basicDataQuestions" :key="q.id" class="input-group full-width">
                {{ renderInput(q, basicDataResponses) }}
                <label class="q-label"
                  >{{ q.question_text }} <span v-if="q.required" class="required">*</span></label
                >
                <p v-if="q.guidance" class="field-help">{{ q.guidance }}</p>

                <input
                  v-if="q.answer_type === 'Short Text'"
                  type="text"
                  class="form-input"
                  v-model="basicDataResponses[q.id]"
                  placeholder="Enter response..."
                />
                <textarea
                  v-else-if="q.answer_type === 'Long Text' || q.answer_type === 'text'"
                  class="form-textarea"
                  rows="4"
                  v-model="basicDataResponses[q.id]"
                  placeholder="Enter detailed response..."
                ></textarea>

                <select
                  v-else-if="q.answer_type === 'Dropdown'"
                  class="form-select"
                  v-model="basicDataResponses[q.id]"
                >
                  <option disabled value="">Select an option...</option>
                  <option v-for="opt in q.options" :key="opt" :value="opt">{{ opt }}</option>
                </select>

                <div
                  v-else-if="
                    q.answer_type === 'Radio' ||
                    q.answer_type === 'single_choice' ||
                    q.answer_type === 'yes_no'
                  "
                  class="radio-pill-group"
                >
                  <label
                    v-for="opt in q.options || ['Yes', 'No']"
                    :key="opt"
                    :class="['radio-pill', { active: basicDataResponses[q.id] === opt }]"
                  >
                    <input
                      type="radio"
                      :value="opt"
                      v-model="basicDataResponses[q.id]"
                      class="hidden-radio"
                    />
                    {{ opt }}
                  </label>
                </div>

                <div
                  v-else-if="q.answer_type === 'Checkbox' || q.answer_type === 'multi_choice'"
                  style="
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                    background: rgba(255, 255, 255, 0.5);
                    padding: 16px;
                    border-radius: 8px;
                    border: 1px solid #e2e8f0;
                    margin-top: 8px;
                  "
                >
                  <label
                    v-for="opt in q.options"
                    :key="opt"
                    style="
                      display: flex;
                      align-items: center;
                      gap: 8px;
                      cursor: pointer;
                      color: #334155;
                      font-size: 14px;
                      font-weight: 500;
                    "
                  >
                    <input
                      type="checkbox"
                      :value="opt"
                      v-model="basicDataResponses[q.id]"
                      style="width: 18px; height: 18px; accent-color: #0d9488"
                    />
                    {{ opt }}
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Step 2: Screening Matrix -->
          <div v-if="currentStep === 2" class="form-section fade-in">
            <div class="section-header-box">
              <h2 class="section-title">Screening Matrix</h2>
              <p class="section-subtitle">
                Answer the following questions to determine if a Full PIA is required.
              </p>
            </div>

            <div class="risk-matrix">
              <div v-for="q in screeningQuestions" :key="q.id" class="matrix-row">
                {{ renderInput(q, screeningResponses) }}
                <div class="matrix-question">
                  <div class="q-text-wrap">
                    <span class="q-num">{{ q.question_number || 'Q' }}</span>
                    <h3>{{ q.question_text }}</h3>
                  </div>
                  <p v-if="q.guidance" class="q-guide">{{ q.guidance }}</p>
                </div>
                <div class="matrix-answer">
                  <div
                    v-if="
                      q.answer_type === 'yes_no' ||
                      q.answer_type === 'single_choice' ||
                      q.answer_type === 'Radio'
                    "
                    class="pill-toggle"
                    style="flex-wrap: wrap"
                  >
                    <label
                      v-for="opt in q.options || ['Yes', 'No']"
                      :key="opt"
                      :class="['toggle-btn', { 'active-yes': screeningResponses[q.id] === opt }]"
                    >
                      <input
                        type="radio"
                        :value="opt"
                        v-model="screeningResponses[q.id]"
                        class="hidden-radio"
                      />
                      {{ opt }}
                    </label>
                  </div>

                  <textarea
                    v-else-if="
                      q.answer_type === 'text' ||
                      q.answer_type === 'Short Text' ||
                      q.answer_type === 'Long Text'
                    "
                    class="form-textarea"
                    rows="3"
                    v-model="screeningResponses[q.id]"
                    placeholder="Enter response..."
                  ></textarea>

                  <div
                    v-else-if="q.answer_type === 'multi_choice' || q.answer_type === 'Checkbox'"
                    style="display: flex; flex-direction: column; gap: 8px"
                  >
                    <label
                      v-for="opt in q.options"
                      :key="opt"
                      style="
                        display: flex;
                        align-items: center;
                        gap: 8px;
                        cursor: pointer;
                        color: #334155;
                        font-size: 14px;
                      "
                    >
                      <input
                        type="checkbox"
                        :value="opt"
                        v-model="screeningResponses[q.id]"
                        style="width: 18px; height: 18px; accent-color: #0d9488"
                      />
                      {{ opt }}
                    </label>
                  </div>

                  <div v-else-if="q.answer_type === 'matrix'" class="matrix-grid-container">
                    <table class="custom-matrix-table">
                      <thead>
                        <tr>
                          <th>Category</th>
                          <th v-for="col in q.options.columns" :key="col">{{ col }}</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="row in q.options.rows" :key="row">
                          <td class="row-label">{{ row }}</td>
                          <td v-for="col in q.options.columns" :key="col" class="checkbox-cell">
                            <input
                              type="checkbox"
                              v-model="screeningResponses[q.id][row]"
                              :value="col"
                              class="matrix-checkbox"
                            />
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="wizard-footer">
          <button class="btn-back" @click="handlePrevStep" :disabled="currentStep === 1">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
            Back
          </button>
          <button class="btn-primary" @click="handleNextStep" :disabled="isLoading">
            {{ currentStep === 2 ? 'Submit Assessment' : 'Save & Continue' }}
            <svg
              v-if="currentStep < 2"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
            <svg
              v-else
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </button>
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
  background-color: #f1f5f9; /* Softer, premium background */
}

/* Top Navbar */
.top-navbar {
  height: 90px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(226, 232, 240, 0.8);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 4px 20px rgba(15, 23, 42, 0.02);
}

.navbar-brand {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.brand-logo-img {
  height: 70px;
  width: auto;
  object-fit: contain;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 24px;
}

.user-profile-menu {
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 12px;
  transition: background-color 0.2s;
}

.user-profile-menu:hover {
  background-color: #f8fafc;
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
.main-body {
  flex: 1;
  display: flex;
}

/* Main Workspace */
.content-area {
  flex: 1;
  padding: 40px 60px;
  max-width: 1100px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

/* Header */
.wizard-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.wizard-title-block h1 {
  font-family: var(--font-family);
  font-size: 28px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.02em;
  margin-bottom: 6px;
}

.wizard-title-block p {
  font-size: 14px;
  color: #64748b;
}

.btn-secondary {
  height: 42px;
  padding: 0 20px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  font-family: var(--font-family);
  font-size: 13px;
  font-weight: 600;
  color: #334155;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(15, 23, 42, 0.02);
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #f8fafc;
  border-color: #94a3b8;
}

/* Progress Stepper */
.wizard-progress-container {
  position: relative;
  padding: 0 10%;
  margin: 10px 0;
}

.progress-track {
  position: absolute;
  top: 18px;
  left: 14%;
  right: 14%;
  height: 4px;
  background-color: #e2e8f0;
  border-radius: 2px;
  z-index: 1;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #0d9488;
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.progress-steps {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
}

.step-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.step-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #ffffff;
  border: 2px solid #cbd5e1;
  color: #64748b;
  font-size: 14px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}

.step-circle svg {
  width: 20px;
  height: 20px;
}

.step-label {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  transition: color 0.3s;
}

.step-node.active .step-circle {
  border-color: #0d9488;
  background-color: #0d9488;
  color: #ffffff;
  box-shadow: 0 0 0 4px rgba(13, 148, 136, 0.15);
}

.step-node.active .step-label {
  color: #0f172a;
  font-weight: 700;
}

.step-node.completed .step-circle {
  background-color: #0f172a;
  border-color: #0f172a;
  color: #ffffff;
}

/* Card Container */
.card-glass {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.6);
  border-radius: 20px;
  padding: 40px;
  box-shadow:
    0 10px 40px rgba(15, 23, 42, 0.04),
    inset 0 0 0 1px rgba(255, 255, 255, 0.5);
}

.section-header-box {
  margin-bottom: 32px;
}

.section-title {
  font-family: var(--font-family);
  font-size: 20px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 6px;
}

.section-subtitle {
  font-size: 14px;
  color: #64748b;
}

.divider {
  height: 1px;
  background: #e2e8f0;
  margin: 36px 0;
}

/* Form Elements */
.form-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 28px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.q-label,
.input-group label {
  font-size: 13.5px;
  font-weight: 600;
  color: #1e293b;
}

.required {
  color: #ef4444;
  margin-left: 2px;
}

.field-help {
  font-size: 12.5px;
  color: #64748b;
  margin-bottom: 4px;
}

.form-input,
.form-select,
.form-textarea {
  width: 100%;
  padding: 0 16px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  font-family: var(--font-family);
  font-size: 14px;
  color: #0f172a;
  outline: none;
  transition: all 0.2s;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.02);
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  border-color: #0d9488;
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
}

.form-input,
.form-select {
  height: 46px;
}

.form-textarea {
  padding: 16px;
  resize: vertical;
}

/* Radio Pill Group */
.radio-pill-group {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 4px;
}

.radio-pill {
  padding: 10px 20px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 9999px;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.02);
}

.radio-pill:hover {
  background: #f8fafc;
  border-color: #94a3b8;
}

.radio-pill.active {
  background: #f0fdfa;
  border-color: #0d9488;
  color: #0f766e;
  box-shadow: 0 0 0 2px rgba(13, 148, 136, 0.1);
}

.hidden-radio {
  display: none;
}

/* Screening Matrix */
.risk-matrix {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.matrix-row {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: stretch;
  padding: 24px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
  gap: 16px;
}

.matrix-row:last-child {
  border-bottom: none;
}

.matrix-question {
  max-width: 100%;
}

.matrix-answer {
  width: 100%;
  background: #f8fafc;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.custom-matrix-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.custom-matrix-table th {
  background: #f1f5f9;
  padding: 12px;
  text-align: center;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  border-bottom: 1px solid #e2e8f0;
}
.custom-matrix-table th:first-child {
  text-align: left;
}

.custom-matrix-table td {
  padding: 12px;
  border-bottom: 1px solid #f1f5f9;
}

.custom-matrix-table .row-label {
  font-size: 13px;
  color: #334155;
  font-weight: 500;
}

.custom-matrix-table .checkbox-cell {
  text-align: center;
}

.matrix-checkbox {
  width: 18px;
  height: 18px;
  accent-color: #0d9488;
  cursor: pointer;
}

.q-text-wrap {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.q-num {
  font-size: 12px;
  font-weight: 800;
  color: #94a3b8;
  background: #f1f5f9;
  padding: 4px 8px;
  border-radius: 6px;
  margin-top: 2px;
}

.matrix-question h3 {
  font-size: 15px;
  font-weight: 600;
  color: #0f172a;
  line-height: 1.4;
}

.q-guide {
  font-size: 13px;
  color: #64748b;
  margin-top: 8px;
  margin-left: 36px;
}

.pill-toggle {
  display: flex;
  background: #f1f5f9;
  padding: 4px;
  border-radius: 12px;
  gap: 4px;
}

.toggle-btn {
  padding: 8px 24px;
  font-size: 13px;
  font-weight: 700;
  color: #64748b;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.toggle-btn.active-yes {
  background: #0f172a;
  color: #ffffff;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.1);
}

.toggle-btn.active-no {
  background: #ffffff;
  color: #0f172a;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.05);
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  background: #f8fafc;
  border: 2px dashed #cbd5e1;
  border-radius: 16px;
  color: #64748b;
  gap: 12px;
}

.empty-state svg {
  width: 48px;
  height: 48px;
  color: #94a3b8;
}

/* Footer Actions */
.wizard-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 10px;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 48px;
  padding: 0 24px;
  background: transparent;
  border: none;
  font-family: var(--font-family);
  font-size: 14.5px;
  font-weight: 700;
  color: #64748b;
  cursor: pointer;
  transition: color 0.2s;
}

.btn-back:hover:not(:disabled) {
  color: #0f172a;
}

.btn-back:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-back svg {
  width: 18px;
  height: 18px;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 10px;
  height: 48px;
  padding: 0 32px;
  background: #0d9488;
  border: none;
  border-radius: 12px;
  font-family: var(--font-family);
  font-size: 14.5px;
  font-weight: 700;
  color: #ffffff;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(13, 148, 136, 0.2);
  transition: all 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #0f766e;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(13, 148, 136, 0.3);
}

.btn-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.btn-primary svg {
  width: 18px;
  height: 18px;
}
</style>
