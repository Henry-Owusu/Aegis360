<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import DpoSidebar from './components/DpoSidebar.vue'
import { dpiaApi } from '@/services/api'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const assessmentId = ref<string>((route.params.id as string))
const isLoading = ref(false)

const title = ref('')
const projectManager = ref('')
const assessmentStatus = ref('')

// Full PIA data
const fullPiaQuestions = ref<any[]>([])
const fullPiaResponses = ref<Record<string, any>>({})

const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref<'success' | 'error'>('success')

const triggerToast = (msg: string, type: 'success' | 'error' = 'success') => {
  toastMessage.value = msg
  toastType.value = type
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 4000)
}

const getOptions = (opts: any) => {
  if (Array.isArray(opts)) return opts
  if (typeof opts === 'string') {
    if (!opts.trim()) return ['Yes', 'No']
    try {
      let sanitized = opts.replace(/'/g, '"')
      return JSON.parse(sanitized)
    } catch(e) {
      return opts.split(',').map(s => s.trim())
    }
  }
  return ['Yes', 'No']
}

const loadData = async () => {
  isLoading.value = true
  try {
    const [metaRes, questionsRes, respRes] = await Promise.all([
      dpiaApi.getAssessment(assessmentId.value),
      dpiaApi.getQuestions('full_pia'),
      dpiaApi.getResponses(assessmentId.value)
    ])
    
    const meta = ('assessment' in metaRes) ? (metaRes as any).assessment : metaRes
    title.value = meta.title
    projectManager.value = meta.project_manager
    assessmentStatus.value = meta.status

    fullPiaQuestions.value = questionsRes.questions || []

    if (respRes.responses) {
      const fResps: Record<string, any> = {}
      for (const [qId, answer] of Object.entries(respRes.responses)) {
        if (fullPiaQuestions.value.find(q => q.id.toString() === qId)) {
          fResps[qId] = answer
        }
      }
      fullPiaResponses.value = fResps
    }

    fullPiaQuestions.value.forEach(q => {
      q.parsedOptions = getOptions(q.options)
      const isMulti = ['Multiple Choice', 'Checkbox', 'multi_choice'].includes(q.answer_type)
      
      if (isMulti) {
        if (!fullPiaResponses.value[q.id]) {
          fullPiaResponses.value[q.id] = []
        } else if (!Array.isArray(fullPiaResponses.value[q.id])) {
          try {
            const parsed = JSON.parse(fullPiaResponses.value[q.id])
            fullPiaResponses.value[q.id] = Array.isArray(parsed) ? parsed : [fullPiaResponses.value[q.id]]
          } catch(e) {
            fullPiaResponses.value[q.id] = [fullPiaResponses.value[q.id]]
          }
        }
      } else {
        if (fullPiaResponses.value[q.id] === undefined) {
          fullPiaResponses.value[q.id] = ''
        }
      }
    })
  } catch (error) {
    console.error('Failed to load full PIA data', error)
    window.alert('Failed to load assessment data')
  }
  isLoading.value = false
}

onMounted(() => {
  loadData()
})

const groupedParts = computed(() => {
  const parts: { title: string, questions: any[] }[] = []
  fullPiaQuestions.value.forEach(q => {
    let part = parts.find(p => p.title === q.section_title)
    if (!part) {
      part = { title: q.section_title, questions: [] }
      parts.push(part)
    }
    part.questions.push(q)
  })
  return parts
})

const activePartIndex = ref(0)
const activePart = computed(() => groupedParts.value[activePartIndex.value])

const handleNext = () => {
  if (activePartIndex.value < groupedParts.value.length - 1) {
    activePartIndex.value++
    document.querySelector('.wizard-content-scroll')?.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const handlePrev = () => {
  if (activePartIndex.value > 0) {
    activePartIndex.value--
    document.querySelector('.wizard-content-scroll')?.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const isPartCompleted = (part: any) => {
  if (!part || !part.questions) return false
  
  const requiredQuestions = part.questions.filter((q: any) => q.required)
  
  if (requiredQuestions.length === 0) {
    return part.questions.some((q: any) => {
      const ans = fullPiaResponses.value[q.id]
      if (Array.isArray(ans)) return ans.length > 0
      return ans !== undefined && ans !== null && String(ans).trim() !== ''
    })
  }

  return requiredQuestions.every((q: any) => {
    const ans = fullPiaResponses.value[q.id]
    if (Array.isArray(ans)) return ans.length > 0
    return ans !== undefined && ans !== null && String(ans).trim() !== ''
  })
}

const handleSaveDraft = async () => {
  isLoading.value = true
  try {
    await dpiaApi.saveResponses(assessmentId.value, fullPiaResponses.value)
    triggerToast('Responses saved successfully!')
  } catch (err) {
    console.error('Error saving responses:', err)
    window.alert('Failed to save responses.')
  }
  isLoading.value = false
}

const confirmAndSubmitFullPia = async () => {
  const incompleteIndex = groupedParts.value.findIndex(part => !isPartCompleted(part))
  
  if (incompleteIndex !== -1) {
    triggerToast(`Cannot submit. Please complete all required questions in Part ${incompleteIndex + 1}.`, 'error')
    activePartIndex.value = incompleteIndex
    document.querySelector('.wizard-content-scroll')?.scrollTo({ top: 0, behavior: 'smooth' })
    return
  }

  isLoading.value = true
  try {
    await dpiaApi.saveResponses(assessmentId.value, fullPiaResponses.value)
    await dpiaApi.reviewAssessment(assessmentId.value, { action: 'Complete Full PIA' })
    triggerToast('Full PIA completed successfully!')
    setTimeout(() => {
      router.push(`/dpo/dpia/${assessmentId.value}/risk`)
    }, 1500)
  } catch (err) {
    console.error('Failed to submit full PIA:', err)
    window.alert('Failed to submit full PIA.')
  }
  isLoading.value = false
}

const handleBack = () => {
  router.push(`/dpo/dpia/${assessmentId.value}`)
}
</script>

<template>
  <div class="dashboard-layout">
    <DpoSidebar />

    <main class="main-content">
      <header class="top-nav">
        <div class="search-bar">
          <button class="btn-back-nav" @click="handleBack">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
            Back to Review
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

      <div class="wizard-container">
        
        <!-- Left Sidebar: Steps -->
        <aside class="wizard-sidebar">
          <div class="wizard-header">
            <h1 class="page-title">Full PIA</h1>
            <p class="page-subtitle">{{ title }}</p>
          </div>
          
          <nav class="steps-nav">
            <button 
              v-for="(part, idx) in groupedParts" 
              :key="idx"
              :class="['step-btn', { active: activePartIndex === idx, completed: isPartCompleted(part) && activePartIndex !== idx }]"
              @click="activePartIndex = idx"
            >
              <div class="step-indicator">
                <svg v-if="isPartCompleted(part) && activePartIndex !== idx" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                  <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
                <span v-else>{{ idx + 1 }}</span>
              </div>
              <div class="step-details">
                <span class="step-name">Part {{ idx + 1 }}</span>
                <span class="step-title" :title="part.title">{{ part.title }}</span>
              </div>
            </button>
          </nav>
        </aside>

        <!-- Right Content: Form -->
        <div class="wizard-content-area">
          <div v-if="isLoading && groupedParts.length === 0" class="loading-state">
            Loading questions...
          </div>
          <div v-else-if="groupedParts.length === 0" class="empty-state">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <p>No Full PIA questions configured.</p>
          </div>
          <div v-else class="wizard-content-scroll">
            
            <div class="form-card fade-in">
              <div class="part-header">
                <h2>Part {{ activePartIndex + 1 }}</h2>
                <p>{{ activePart?.title }}</p>
              </div>

              <div class="form-section">
                <div v-for="(q, idx) in activePart?.questions" :key="q.id" class="question-block">
                  <div class="q-header">
                    <div class="q-text-wrap">
                      <span class="q-num">{{ q.question_number || 'Q' + (idx + 1) }}</span>
                      <label class="q-label">{{ q.question_text }}</label>
                    </div>
                    <span class="q-required" v-if="q.required">*Required</span>
                  </div>
                  <p v-if="q.guidance" class="q-guide">{{ q.guidance }}</p>
                  
                  <div class="q-input">
                    <template v-if="q.answer_type === 'Text' || q.answer_type === 'Short Text' || q.answer_type === 'text'">
                      <input type="text" class="input-field" v-model="fullPiaResponses[q.id]" placeholder="Enter answer..." />
                    </template>
                    <template v-else-if="q.answer_type === 'Long Text' || q.answer_type === 'long_text'">
                      <textarea class="textarea-field" rows="4" v-model="fullPiaResponses[q.id]" placeholder="Enter detailed answer..."></textarea>
                    </template>
                    
                    <template v-else-if="q.answer_type === 'Single Choice' || q.answer_type === 'single_choice' || q.answer_type === 'Boolean' || q.answer_type === 'Radio' || q.answer_type === 'radio' || q.answer_type === 'yes_no' || q.answer_type === 'Dropdown'">
                      <div class="radio-pill-group">
                        <label 
                          v-for="opt in q.parsedOptions" 
                          :key="opt" 
                          :class="['radio-pill', { active: fullPiaResponses[q.id] === opt }]"
                        >
                          <input 
                            type="radio" 
                            :value="opt" 
                            v-model="fullPiaResponses[q.id]" 
                            class="hidden-radio"
                          />
                          {{ opt }}
                        </label>
                      </div>
                    </template>
                    
                    <template v-else-if="q.answer_type === 'Multiple Choice' || q.answer_type === 'Checkbox' || q.answer_type === 'multi_choice'">
                      <div class="premium-checkbox-group">
                        <label 
                          v-for="opt in q.parsedOptions" 
                          :key="opt" 
                          :class="['checkbox-pill', { active: fullPiaResponses[q.id]?.includes(opt) }]"
                        >
                          <input 
                            type="checkbox" 
                            :value="opt" 
                            v-model="fullPiaResponses[q.id]" 
                            class="hidden-checkbox"
                          />
                          <div class="checkbox-indicator">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" v-if="fullPiaResponses[q.id]?.includes(opt)">
                              <polyline points="20 6 9 17 4 12"></polyline>
                            </svg>
                          </div>
                          <span>{{ opt }}</span>
                        </label>
                      </div>
                    </template>

                    <template v-else>
                      <input type="text" class="input-field" v-model="fullPiaResponses[q.id]" placeholder="Enter answer..." />
                    </template>
                  </div>
                </div>
              </div>
            </div>

            <!-- Wizard Footer -->
            <div class="wizard-footer">
              <button 
                class="btn-nav" 
                @click="handlePrev" 
                :disabled="activePartIndex === 0 || isLoading"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="19" y1="12" x2="5" y2="12"></line>
                  <polyline points="12 19 5 12 12 5"></polyline>
                </svg>
                Previous Part
              </button>
              
              <div class="footer-actions-right">
                <button class="btn-outline-primary" @click="handleSaveDraft" :disabled="isLoading">
                  Save Draft
                </button>
                
                <button 
                  v-if="activePartIndex < groupedParts.length - 1" 
                  class="btn-primary" 
                  @click="handleNext" 
                  :disabled="isLoading"
                >
                  Next Part
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                    <polyline points="12 5 19 12 12 19"></polyline>
                  </svg>
                </button>
                
                <button 
                  v-else 
                  class="btn-submit" 
                  @click="confirmAndSubmitFullPia" 
                  :disabled="isLoading"
                >
                  Submit Full PIA
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="20 6 9 17 4 12"></polyline>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Toast Notification -->
      <transition name="toast-slide">
        <div v-if="showToast" class="toast-notification" :class="toastType">
          <svg v-if="toastType === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          {{ toastMessage }}
        </div>
      </transition>
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
  font-size: 14.5px;
  font-weight: 700;
  color: #64748b;
  cursor: pointer;
  padding: 8px 0;
}

.btn-back-nav:hover {
  color: #0f172a;
}

.btn-back-nav svg {
  width: 18px;
  height: 18px;
}

/* User Profile Nav */
.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #0f172a;
}

.user-role {
  font-size: 12px;
  color: #64748b;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #e2e8f0;
}

/* Wizard Layout */
.wizard-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.wizard-sidebar {
  width: 320px;
  background: #ffffff;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.wizard-header {
  padding: 32px 24px 24px;
  border-bottom: 1px solid #f1f5f9;
}

.page-title {
  font-size: 24px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.02em;
  margin: 0 0 4px 0;
}

.page-subtitle {
  font-size: 14px;
  color: #64748b;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.steps-nav {
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.step-btn {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  background: transparent;
  border: none;
  border-radius: 12px;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s;
}

.step-btn:hover {
  background: #f8fafc;
}

.step-btn.active {
  background: #fff7ed;
  box-shadow: 0 2px 8px rgba(245, 132, 37, 0.08);
}

.step-indicator {
  width: 28px;
  height: 28px;
  flex-shrink: 0;
  border-radius: 50%;
  background: #f1f5f9;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  transition: all 0.2s;
}

.step-btn.active .step-indicator {
  background: #F58425;
  color: #ffffff;
}

.step-btn.completed .step-indicator {
  background: #22c55e;
  color: #ffffff;
}

.step-indicator svg {
  width: 14px;
  height: 14px;
}

.step-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
  overflow: hidden;
}

.step-name {
  font-size: 13px;
  font-weight: 700;
  color: #64748b;
}

.step-btn.active .step-name {
  color: #F58425;
}

.step-title {
  font-size: 14px;
  font-weight: 600;
  color: #0f172a;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Wizard Content */
.wizard-content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f8fafc;
  overflow: hidden;
}

.wizard-content-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 40px;
}

.part-header {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 2px solid #f1f5f9;
}

.part-header h2 {
  font-size: 20px;
  font-weight: 800;
  color: #F58425;
  margin: 0 0 8px 0;
}

.part-header p {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  margin: 0;
  line-height: 1.4;
}

.form-card {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.04);
  border: 1px solid #e2e8f0;
  padding: 40px;
  max-width: 900px;
  margin: 0 auto 32px auto;
}

.question-block {
  margin-bottom: 40px;
}

.question-block:last-child {
  margin-bottom: 0;
}

.q-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
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

.q-label {
  font-size: 15px;
  font-weight: 600;
  color: #0f172a;
  line-height: 1.5;
}

.q-required {
  font-size: 12px;
  font-weight: 700;
  color: #ef4444;
  background: #fef2f2;
  padding: 4px 8px;
  border-radius: 6px;
}

.q-guide {
  font-size: 13.5px;
  color: #64748b;
  margin: 0 0 16px 36px;
  line-height: 1.5;
}

.q-input {
  margin-left: 36px;
}

.input-field, .textarea-field {
  width: 100%;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  padding: 16px;
  font-size: 15px;
  font-family: inherit;
  color: #0f172a;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.input-field:focus, .textarea-field:focus {
  outline: none;
  border-color: #F58425;
  background: #ffffff;
  box-shadow: 0 0 0 4px rgba(245, 132, 37, 0.15);
}

/* Premium Radio Pills */
.radio-pill-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.hidden-radio, .hidden-checkbox {
  display: none;
}

.radio-pill {
  padding: 12px 24px;
  background: #f1f5f9;
  border: 2px solid transparent;
  border-radius: 100px;
  font-size: 14.5px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
}

.radio-pill:hover {
  background: #e2e8f0;
}

.radio-pill.active {
  background: #fff7ed;
  border-color: #F58425;
  color: #F58425;
  box-shadow: 0 4px 12px rgba(245, 132, 37, 0.15);
}

/* Premium Checkbox Group */
.premium-checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.checkbox-pill {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 500;
  color: #334155;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
}

.checkbox-pill:hover {
  border-color: #cbd5e1;
  background: #f1f5f9;
}

.checkbox-pill.active {
  background: #fff7ed;
  border-color: #F58425;
  color: #9a4c0c;
}

.checkbox-indicator {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  border: 2px solid #cbd5e1;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  background: #ffffff;
}

.checkbox-pill.active .checkbox-indicator {
  background: #F58425;
  border-color: #F58425;
  color: #ffffff;
}

.checkbox-indicator svg {
  width: 14px;
  height: 14px;
}

.wizard-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 16px;
  max-width: 900px;
  margin: 0 auto;
}

.footer-actions-right {
  display: flex;
  gap: 16px;
}

.btn-nav {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 48px;
  padding: 0 24px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  font-size: 14.5px;
  font-weight: 700;
  color: #475569;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

.btn-nav:hover:not(:disabled) {
  background: #f8fafc;
  border-color: #94a3b8;
  color: #0f172a;
}

.btn-nav:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-nav svg {
  width: 18px;
  height: 18px;
}

.btn-primary, .btn-submit {
  display: flex;
  align-items: center;
  gap: 10px;
  height: 48px;
  padding: 0 32px;
  background: #0f172a;
  border: none;
  border-radius: 12px;
  font-family: inherit;
  font-size: 14.5px;
  font-weight: 700;
  color: #ffffff;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.2);
  transition: all 0.2s;
}

.btn-submit {
  background: #22c55e;
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.2);
}

.btn-primary:hover:not(:disabled) {
  background: #1e293b;
  transform: translateY(-2px);
}

.btn-submit:hover:not(:disabled) {
  background: #16a34a;
  transform: translateY(-2px);
}

.btn-primary:disabled, .btn-submit:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.btn-outline-primary {
  display: flex;
  align-items: center;
  height: 48px;
  padding: 0 24px;
  background: #fff7ed;
  border: 2px solid #F58425;
  border-radius: 12px;
  font-family: inherit;
  font-size: 14.5px;
  font-weight: 700;
  color: #F58425;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-outline-primary:hover:not(:disabled) {
  background: #F58425;
  color: #ffffff;
}

.btn-outline-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-state, .empty-state {
  text-align: center;
  color: #64748b;
  padding: 60px;
}

.fade-in { animation: fadeIn 0.4s ease-out forwards; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

/* Toast Notification Styles */
.toast-notification {
  position: absolute;
  bottom: 40px;
  right: 40px;
  color: #ffffff;
  padding: 16px 24px;
  border-radius: 12px;
  font-size: 14.5px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 1000;
}

.toast-notification.success {
  background: #22c55e;
  box-shadow: 0 10px 25px rgba(34, 197, 94, 0.4);
}

.toast-notification.error {
  background: #ef4444;
  box-shadow: 0 10px 25px rgba(239, 68, 68, 0.4);
}

.toast-notification svg {
  width: 20px;
  height: 20px;
}

.toast-slide-enter-active,
.toast-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-slide-enter-from,
.toast-slide-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}
</style>
