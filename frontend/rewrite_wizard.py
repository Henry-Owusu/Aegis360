import os

FILE_PATH = "/Users/henry/Aegis360/frontend/src/views/dpia/DpiaAssessmentView.vue"

with open(FILE_PATH, 'r') as f:
    lines = f.readlines()

# Find where <style scoped> starts
style_start = -1
for i, line in enumerate(lines):
    if "<style scoped>" in line:
        style_start = i
        break

style_content = "".join(lines[style_start:])

new_script_template = """<script setup lang="ts">
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
const fullPiaQuestions = ref<any[]>([])

// Responses dicts
const basicDataResponses = ref<Record<string, any>>({})
const screeningResponses = ref<Record<string, any>>({})
const fullPiaResponses = ref<Record<string, any>>({})

const isLoading = ref(false)

const loadQuestions = async () => {
  try {
    const [bd, sc, fp] = await Promise.all([
      dpiaApi.getQuestions('basic_data'),
      dpiaApi.getQuestions('screening'),
      dpiaApi.getQuestions('full_pia')
    ])
    basicDataQuestions.value = bd.questions || []
    screeningQuestions.value = sc.questions || []
    fullPiaQuestions.value = fp.questions || []
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
      alert("Title and Project Manager are required to create a draft.")
      return
    }
    const res = await dpiaApi.createAssessment({ title: title.value, project_manager: projectManager.value })
    assessmentId.value = res.id
  }
  
  if (assessmentId.value) {
    if (currentStep.value === 1) await dpiaApi.saveResponses(assessmentId.value, basicDataResponses.value)
    if (currentStep.value === 2) await dpiaApi.saveResponses(assessmentId.value, screeningResponses.value)
    if (currentStep.value === 3) await dpiaApi.saveResponses(assessmentId.value, fullPiaResponses.value)
  }
  window.alert('DPIA Assessment Draft saved successfully!')
}

const handleNextStep = async () => {
  isLoading.value = true
  if (currentStep.value === 1) {
    if (!assessmentId.value) {
      if (!title.value || !projectManager.value) {
        alert("Title and Project Manager are required to proceed.")
        isLoading.value = false
        return
      }
      const res = await dpiaApi.createAssessment({ title: title.value, project_manager: projectManager.value })
      assessmentId.value = res.id
    }
    await dpiaApi.saveResponses(assessmentId.value, basicDataResponses.value)
    currentStep.value = 2
  } else if (currentStep.value === 2) {
    await dpiaApi.saveResponses(assessmentId.value, screeningResponses.value)
    currentStep.value = 3
  } else {
    await dpiaApi.saveResponses(assessmentId.value, fullPiaResponses.value)
    window.alert('DPIA Assessment submitted successfully for DPO Review!')
    router.push('/pm/dashboard')
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
    vModelTarget[question.id] = question.answer_type === 'Checkbox' ? [] : ''
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
        <div class="user-profile">
          <div class="avatar">PM</div>
          <div class="user-info">
            <span class="user-name">Project Manager</span>
          </div>
        </div>
        <button class="logout-btn" @click="handleLogout" title="Logout">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
          </svg>
        </button>
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
            <button class="btn-secondary" @click="handleSaveDraft" :disabled="isLoading">Save Draft</button>
          </div>
        </div>

        <!-- Wizard Progress Bar -->
        <div class="wizard-progress">
          <div class="progress-steps">
            <div :class="['step', { active: currentStep >= 1, completed: currentStep > 1 }]">
              <div class="step-indicator">1</div>
              <span class="step-label">Basic Data</span>
            </div>
            <div class="step-line" :class="{ active: currentStep >= 2 }"></div>
            
            <div :class="['step', { active: currentStep >= 2, completed: currentStep > 2 }]">
              <div class="step-indicator">2</div>
              <span class="step-label">Screening Matrix</span>
            </div>
            <div class="step-line" :class="{ active: currentStep >= 3 }"></div>
            
            <div :class="['step', { active: currentStep >= 3 }]">
              <div class="step-indicator">3</div>
              <span class="step-label">Full PIA</span>
            </div>
          </div>
        </div>

        <div class="wizard-content">
          <!-- Step 1: Basic Data -->
          <div v-if="currentStep === 1" class="form-section fade-in">
            <h2 class="section-title">Core Properties</h2>
            
            <div class="form-grid">
              <div class="input-group full-width">
                <label>Assessment Title <span class="required">*</span></label>
                <input type="text" v-model="title" class="form-input" placeholder="Enter project or assessment name" />
              </div>

              <div class="input-group">
                <label>Project Manager <span class="required">*</span></label>
                <input type="text" v-model="projectManager" class="form-input" placeholder="Name of Project Manager" />
              </div>
            </div>

            <h2 class="section-title" style="margin-top: 32px;" v-if="basicDataQuestions.length > 0">Additional Details</h2>
            <div class="form-grid">
              <div v-for="q in basicDataQuestions" :key="q.id" class="input-group full-width">
                {{ renderInput(q, basicDataResponses) }}
                <label>{{ q.question_text }} <span v-if="q.required" class="required">*</span></label>
                <p v-if="q.guidance" class="field-help">{{ q.guidance }}</p>
                
                <input v-if="q.answer_type === 'Short Text'" type="text" class="form-input" v-model="basicDataResponses[q.id]" />
                <textarea v-else-if="q.answer_type === 'Long Text'" class="form-input" rows="4" v-model="basicDataResponses[q.id]"></textarea>
                
                <select v-else-if="q.answer_type === 'Dropdown'" class="form-input" v-model="basicDataResponses[q.id]">
                  <option v-for="opt in q.options" :key="opt" :value="opt">{{ opt }}</option>
                </select>
                
                <div v-else-if="q.answer_type === 'Radio'" class="radio-group horizontal">
                  <label v-for="opt in q.options" :key="opt" class="radio-label">
                    <input type="radio" :value="opt" v-model="basicDataResponses[q.id]"> {{ opt }}
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Step 2: Screening Matrix -->
          <div v-if="currentStep === 2" class="form-section fade-in">
            <h2 class="section-title">Screening Questions</h2>
            <div class="risk-matrix">
              <div v-for="q in screeningQuestions" :key="q.id" class="matrix-row">
                {{ renderInput(q, screeningResponses) }}
                <div class="matrix-question">
                  <h3>{{ q.question_text }}</h3>
                  <p v-if="q.guidance">{{ q.guidance }}</p>
                </div>
                <div class="matrix-toggle">
                  <div class="toggle-switch">
                    <input type="radio" :id="`yes_${q.id}`" value="Yes" v-model="screeningResponses[q.id]" />
                    <label :for="`yes_${q.id}`">Yes</label>
                    <input type="radio" :id="`no_${q.id}`" value="No" v-model="screeningResponses[q.id]" />
                    <label :for="`no_${q.id}`">No</label>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Step 3: Full PIA -->
          <div v-if="currentStep === 3" class="form-section fade-in">
            <h2 class="section-title">Full PIA Questionnaire</h2>
            <p v-if="fullPiaQuestions.length === 0" class="field-help">No questions configured for Full PIA.</p>
            <div class="form-grid">
              <div v-for="q in fullPiaQuestions" :key="q.id" class="input-group full-width">
                {{ renderInput(q, fullPiaResponses) }}
                <label>{{ q.question_text }} <span v-if="q.required" class="required">*</span></label>
                <p v-if="q.guidance" class="field-help">{{ q.guidance }}</p>
                
                <input v-if="q.answer_type === 'Short Text'" type="text" class="form-input" v-model="fullPiaResponses[q.id]" />
                <textarea v-else-if="q.answer_type === 'Long Text'" class="form-input" rows="4" v-model="fullPiaResponses[q.id]"></textarea>
                
                <select v-else-if="q.answer_type === 'Dropdown'" class="form-input" v-model="fullPiaResponses[q.id]">
                  <option v-for="opt in q.options" :key="opt" :value="opt">{{ opt }}</option>
                </select>
                
                <div v-else-if="q.answer_type === 'Radio'" class="radio-group horizontal">
                  <label v-for="opt in q.options" :key="opt" class="radio-label">
                    <input type="radio" :value="opt" v-model="fullPiaResponses[q.id]"> {{ opt }}
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="wizard-footer">
          <button class="btn-outline" @click="handlePrevStep" :disabled="currentStep === 1">Back</button>
          <button class="btn-primary" @click="handleNextStep" :disabled="isLoading">
            {{ currentStep === 3 ? 'Submit Assessment' : 'Save & Continue' }}
          </button>
        </div>
      </main>
    </div>
  </div>
</template>
"""

with open(FILE_PATH, 'w') as f:
    f.write(new_script_template)
    f.write("\n")
    f.write(style_content)
