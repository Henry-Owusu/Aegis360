<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import DpoSidebar from './components/DpoSidebar.vue'
import { dpiaApi } from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const sections = ref([
  { id: 'basic_data', name: 'Basic Data', active: true },
  { id: 'screening', name: 'Screening', active: false },
  { id: 'full_pia', name: 'Full PIA', active: false }
])

const activeSectionId = computed(() => sections.value.find(s => s.active)?.id || 'basic_data')

const questions = ref<any[]>([])
const isLoading = ref(false)

const isPreviewing = ref(false)
const isAddingQuestion = ref(false)
const isEditingQuestion = ref(false)
const editingQuestionId = ref<number | null>(null)

const newQuestion = ref({
  section_title: '',
  question_number: '',
  question_text: '',
  guidance: '',
  answer_type: 'Short Text',
  required: true,
  display_order: 0,
  options: [] as string[]
})
const newOptionText = ref('')

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const loadQuestions = async () => {
  isLoading.value = true
  try {
    const res = await dpiaApi.getQuestions(activeSectionId.value)
    questions.value = res.questions || []
  } catch (error) {
    console.error('Failed to load questions', error)
  } finally {
    isLoading.value = false
  }
}

const selectSection = (id: string) => {
  sections.value.forEach(s => s.active = s.id === id)
  loadQuestions()
}

const addOption = () => {
  if (newOptionText.value.trim()) {
    newQuestion.value.options.push(newOptionText.value.trim())
    newOptionText.value = ''
  }
}

const removeOption = (idx: number) => {
  newQuestion.value.options.splice(idx, 1)
}

const openAddPanel = () => {
  isEditingQuestion.value = false
  editingQuestionId.value = null
  newQuestion.value = {
    section_title: '',
    question_number: '',
    question_text: '',
    guidance: '',
    answer_type: 'Short Text',
    required: true,
    display_order: questions.value.length * 10 + 10,
    options: []
  }
  isAddingQuestion.value = true
}

const handleEditQuestion = (q: any) => {
  isEditingQuestion.value = true
  editingQuestionId.value = q.id
  newQuestion.value = {
    section_title: q.section_title || '',
    question_number: q.question_number || '',
    question_text: q.question_text || '',
    guidance: q.guidance || '',
    answer_type: q.answer_type || 'Short Text',
    required: q.required !== false,
    display_order: q.display_order || 0,
    options: q.options ? [...q.options] : []
  }
  isAddingQuestion.value = true
}

const handleDeleteQuestion = async (id: number) => {
  if (!confirm('Are you sure you want to delete this question?')) return
  try {
    await dpiaApi.deleteQuestion(id)
    await loadQuestions()
  } catch (error) {
    console.error('Failed to delete question', error)
  }
}

const handleSaveQuestion = async () => {
  if (newQuestion.value.question_text.trim() === '') return
  if (newQuestion.value.question_number.trim() === '') return
  if (newQuestion.value.section_title.trim() === '') return
  
  try {
    const payload = {
      ...newQuestion.value,
      section: activeSectionId.value,
      options: ['Radio', 'Checkbox', 'Dropdown'].includes(newQuestion.value.answer_type) ? newQuestion.value.options : null
    }
    
    if (isEditingQuestion.value && editingQuestionId.value) {
      await dpiaApi.updateQuestion(editingQuestionId.value, payload)
    } else {
      await dpiaApi.createQuestion(payload)
    }
    
    isAddingQuestion.value = false
    await loadQuestions()
  } catch (error) {
    console.error('Failed to save question', error)
  }
}

onMounted(() => {
  loadQuestions()
})
</script>

<template>
  <div class="dashboard-layout">
    <!-- Left Sidebar -->
    <DpoSidebar />

    <!-- Main Content Area -->
    <main class="main-content">
      <!-- Top Navigation -->
      <header class="top-nav">
        <div class="search-bar">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input type="text" placeholder="Search ERP data..." />
        </div>

        <div class="nav-actions">
          <button class="icon-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
            <span class="notification-dot"></span>
          </button>

          <div class="user-profile" @click="handleLogout">
            <div class="user-info">
              <span class="user-name">{{ authStore.user.name }}</span>
              <span class="user-role">{{ authStore.primaryRole }}</span>
            </div>
            <img :src="authStore.user.avatar" alt="Profile" class="avatar" />
          </div>
        </div>
      </header>

      <div class="dashboard-scroll-area">
        <!-- Header -->
        <div class="dashboard-header">
          <div>
            <h1 class="page-title">Questionnaire Builder</h1>
            <p class="page-subtitle">Manage dynamic questions for DPIA sections.</p>
          </div>
          <div style="display: flex; gap: 12px;">
            <button class="btn-outline" @click="isPreviewing = true">
              Preview Section
            </button>
            <button class="btn-primary" @click="openAddPanel">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="btn-icon-svg" style="width: 16px; height: 16px;">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
              ADD QUESTION
            </button>
          </div>
        </div>

        <div class="builder-container">
          <!-- Section Tabs -->
          <div class="section-tabs">
            <button 
              v-for="s in sections" 
              :key="s.id" 
              :class="['tab-btn', { active: s.active }]" 
              @click="selectSection(s.id)"
            >
              {{ s.name }}
            </button>
          </div>

          <div class="workspace-grid">
            <!-- Questions List -->
            <div class="questions-list">
              <div v-if="isLoading" class="empty-state">Loading questions...</div>
              <div v-else-if="questions.length === 0" class="empty-state">No questions found in this section.</div>
              <div v-else class="question-card" v-for="q in questions" :key="q.id">
                <div class="q-header">
                  <div style="display: flex; align-items: center; gap: 12px;">
                    <span class="q-number">{{ q.question_number }}</span>
                    <span class="q-type">{{ q.answer_type }}</span>
                    <span v-if="q.required" class="q-badge required">Required</span>
                  </div>
                  <div class="q-actions" style="margin-left: auto; display: flex; gap: 8px;">
                    <button class="icon-btn" @click="handleEditQuestion(q)" title="Edit">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px;">
                        <path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"></path>
                      </svg>
                    </button>
                    <button class="icon-btn danger" @click="handleDeleteQuestion(q.id)" title="Delete">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px;">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                      </svg>
                    </button>
                  </div>
                </div>
                <h3 class="q-title">{{ q.question_text }}</h3>
                <p class="q-subtitle">{{ q.section_title }}</p>
                <p v-if="q.guidance" class="q-guidance">{{ q.guidance }}</p>
                <div v-if="q.options && q.options.length" class="q-options">
                  <span v-for="opt in q.options" :key="opt" class="q-option-pill">{{ opt }}</span>
                </div>
              </div>
            </div>

            <!-- Add Question Panel -->
            <div class="properties-panel" v-if="isAddingQuestion">
              <div class="panel-header">
                <h3>{{ isEditingQuestion ? 'Edit Question' : 'Add New Question' }}</h3>
                <button class="close-btn" @click="isAddingQuestion = false">×</button>
              </div>
              <div class="panel-body">
                <div class="form-group">
                  <label>Question Number / ID</label>
                  <input type="text" v-model="newQuestion.question_number" placeholder="e.g. 1.1">
                </div>
                <div class="form-group">
                  <label>Group / Section Title</label>
                  <input type="text" v-model="newQuestion.section_title" placeholder="e.g. Project Details">
                </div>
                <div class="form-group">
                  <label>Question Text</label>
                  <textarea v-model="newQuestion.question_text" rows="3" placeholder="Enter question"></textarea>
                </div>
                <div class="form-group">
                  <label>Guidance (Optional)</label>
                  <textarea v-model="newQuestion.guidance" rows="2" placeholder="Helpful context"></textarea>
                </div>
                <div class="form-group">
                  <label>Answer Type</label>
                  <select v-model="newQuestion.answer_type">
                    <option>Short Text</option>
                    <option>Long Text</option>
                    <option>Radio</option>
                    <option>Checkbox</option>
                    <option>Dropdown</option>
                    <option>Date</option>
                    <option>User Search</option>
                  </select>
                </div>
                
                <div v-if="['Radio', 'Checkbox', 'Dropdown'].includes(newQuestion.answer_type)" class="form-group options-group">
                  <label>Options</label>
                  <div class="options-list">
                    <div v-for="(opt, idx) in newQuestion.options" :key="idx" class="option-item">
                      <span>{{ opt }}</span>
                      <button class="btn-icon" @click="removeOption(idx)">×</button>
                    </div>
                  </div>
                  <div class="add-option">
                    <input type="text" v-model="newOptionText" placeholder="New option" @keyup.enter="addOption">
                    <button class="btn-outline btn-sm" @click="addOption">Add</button>
                  </div>
                </div>
                
                <div class="form-group checkbox-group">
                  <label>
                    <input type="checkbox" v-model="newQuestion.required">
                    Required Question
                  </label>
                </div>
                
                <div class="form-group">
                  <label>Display Order</label>
                  <input type="number" v-model="newQuestion.display_order">
                </div>
                
                <button class="btn-primary full-width mt-4" @click="handleSaveQuestion">
                  {{ isEditingQuestion ? 'Update Question' : 'Save Question' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Preview Modal -->
        <div v-if="isPreviewing" class="modal-overlay" @click="isPreviewing = false">
          <div class="modal-content preview-modal" @click.stop>
            <div class="modal-header">
              <h2>Preview: {{ sections.find(s => s.active)?.name }}</h2>
              <button class="close-btn" @click="isPreviewing = false">×</button>
            </div>
            <div class="modal-body preview-body">
              <div class="form-grid">
                <div v-for="q in questions" :key="q.id" class="input-group full-width" style="margin-bottom: 24px;">
                  <label style="font-weight: 600; color: #1e293b; display: block; margin-bottom: 8px;">
                    {{ q.question_number }}. {{ q.question_text }}
                    <span v-if="q.required" class="required" style="color: #ef4444;">*</span>
                  </label>
                  <p v-if="q.guidance" class="field-help" style="color: #64748b; font-size: 13px; margin-bottom: 12px; font-style: italic;">
                    {{ q.guidance }}
                  </p>
                  
                  <input v-if="q.answer_type === 'Short Text'" type="text" class="form-input" style="width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px;" placeholder="Short text answer..." disabled />
                  <textarea v-else-if="q.answer_type === 'Long Text'" class="form-input" rows="4" style="width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px;" placeholder="Long text answer..." disabled></textarea>
                  
                  <select v-else-if="q.answer_type === 'Dropdown'" class="form-input" style="width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 6px;" disabled>
                    <option v-for="opt in q.options" :key="opt" :value="opt">{{ opt }}</option>
                  </select>
                  
                  <div v-else-if="q.answer_type === 'Radio'" class="radio-group horizontal" style="display: flex; gap: 16px; flex-wrap: wrap;">
                    <label v-for="opt in q.options" :key="opt" class="radio-label" style="display: flex; align-items: center; gap: 6px; cursor: not-allowed; color: #475569;">
                      <input type="radio" disabled> {{ opt }}
                    </label>
                  </div>

                  <div v-else-if="q.answer_type === 'Checkbox'" class="checkbox-group horizontal" style="display: flex; gap: 16px; flex-wrap: wrap;">
                    <label v-for="opt in q.options" :key="opt" class="checkbox-label" style="display: flex; align-items: center; gap: 6px; cursor: not-allowed; color: #475569;">
                      <input type="checkbox" disabled> {{ opt }}
                    </label>
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button class="btn-outline" @click="isPreviewing = false">Close Preview</button>
            </div>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<style scoped>
/* Builder specific styles injected before dashboard styles */
.builder-container {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.section-tabs {
  display: inline-flex;
  gap: 4px;
  background: #e2e8f0;
  padding: 6px;
  border-radius: 12px;
  align-self: flex-start;
}

.tab-btn {
  background: transparent;
  border: none;
  color: #64748b;
  font-size: 14px;
  font-weight: 600;
  padding: 8px 24px;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.tab-btn:hover {
  color: #0f172a;
}

.tab-btn.active {
  background: #ffffff;
  color: #0f172a;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.workspace-grid {
  display: flex;
  gap: 32px;
  align-items: flex-start;
}

.questions-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: #94a3b8;
  background: #ffffff;
  border-radius: 16px;
  border: 2px dashed #e2e8f0;
  font-size: 15px;
  font-weight: 500;
}

.question-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.question-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: #f58425;
  opacity: 0;
  transition: opacity 0.3s;
}

.question-card:hover {
  border-color: #cbd5e1;
  transform: translateY(-2px);
  box-shadow: 0 12px 24px -4px rgba(15, 23, 42, 0.05);
}

.question-card:hover::before {
  opacity: 1;
}

.q-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.q-number {
  background: #fef3c7;
  color: #d97706;
  padding: 4px 10px;
  border-radius: 20px;
  font-family: 'Inter', monospace;
  font-size: 13px;
  font-weight: 700;
}

.q-type {
  font-size: 13px;
  color: #0f172a;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.q-badge {
  font-size: 11px;
  padding: 4px 10px;
  border-radius: 20px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.q-badge.required {
  background: #fee2e2;
  color: #b91c1c;
}

.q-title {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.q-subtitle {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  margin: 0 0 8px 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.q-guidance {
  font-size: 14px;
  color: #475569;
  margin: 0 0 20px 0;
  line-height: 1.6;
}

.q-options {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px dashed #e2e8f0;
}

.q-option-pill {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  color: #475569;
}

/* Properties Panel */
.properties-panel {
  width: 380px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 32px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05);
}

.panel-header {
  padding: 24px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
  border-radius: 16px 16px 0 0;
}

.panel-header h3 {
  font-size: 16px;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 24px;
  cursor: pointer;
  transition: color 0.2s;
  line-height: 1;
}

.close-btn:hover {
  color: #ef4444;
}

.panel-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: #475569;
}

.form-group input[type="text"],
.form-group input[type="number"],
.form-group select,
.form-group textarea {
  background: #ffffff;
  border: 1px solid #cbd5e1;
  color: #0f172a;
  padding: 12px 14px;
  border-radius: 8px;
  font-family: inherit;
  font-size: 14px;
  transition: all 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #f58425;
  box-shadow: 0 0 0 3px rgba(245, 132, 37, 0.1);
}

.options-group {
  background: #f8fafc;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 16px;
}

.option-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #0f172a;
  box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}

.btn-icon {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 6px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.btn-icon:hover {
  color: #ef4444;
  background: #fee2e2;
}

.add-option {
  display: flex;
  gap: 12px;
}

.checkbox-group {
  flex-direction: row;
  align-items: center;
  background: #f8fafc;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  color: #0f172a;
  font-size: 14px;
  font-weight: 600;
  margin: 0;
}

.checkbox-group input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #f58425;
  cursor: pointer;
}

.full-width {
  width: 100%;
}
.mt-4 {
  margin-top: 24px;
}

.btn-outline {
  background: transparent;
  color: #0f172a;
  border: 1px solid #cbd5e1;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-outline:hover {
  background: #f8fafc;
  border-color: #94a3b8;
}

.btn-sm {
  padding: 8px 16px;
}

.dashboard-layout {
  display: flex;
  height: 100vh;
  background-color: #f8f9fa;
  font-family: 'Inter', system-ui, sans-serif;
  color: #1e293b;
  overflow: hidden;
}

/* Main Content Area */
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
}

.search-bar {
  display: flex;
  align-items: center;
  background: #f1f5f9;
  border-radius: 8px;
  padding: 0 16px;
  width: 380px;
  height: 40px;
}

.search-icon {
  width: 16px;
  height: 16px;
  color: #94a3b8;
  margin-right: 12px;
}

.search-bar input {
  border: none;
  background: transparent;
  width: 100%;
  font-size: 14px;
  color: #0f172a;
  outline: none;
}

.search-bar input::placeholder {
  color: #94a3b8;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 24px;
}

.icon-btn {
  position: relative;
  background: transparent;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 4px;
}

.icon-btn svg {
  width: 22px;
  height: 22px;
}

.notification-dot {
  position: absolute;
  top: 4px;
  right: 6px;
  width: 8px;
  height: 8px;
  background: #ef4444;
  border-radius: 50%;
  border: 2px solid #ffffff;
}

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
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
}

/* Dashboard Scroll Area */
.dashboard-scroll-area {
  padding: 32px;
  overflow-y: auto;
  flex: 1;
}

/* Dashboard Header */
.dashboard-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 32px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 6px;
}

.page-subtitle {
  font-size: 15px;
  color: #64748b;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #0f172a;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.02em;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #1e293b;
}

.btn-icon {
  width: 16px;
  height: 16px;
}

/* Metrics Row */
.metrics-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 40px;
}

.metric-card {
  border-radius: 12px;
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.bg-light { background: #f1f5f9; }
.bg-red-light { background: #fee2e2; }
.bg-gold { background: #d97706; color: #ffffff; }

.metric-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.metric-label {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: #475569;
}

.metric-value {
  font-size: 42px;
  font-weight: 800;
  line-height: 1;
  color: #0f172a;
}

.value-row {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.trend {
  font-size: 14px;
  font-weight: 600;
}

.text-red { color: #b91c1c; }
.text-gold-dark { color: #ffffff; }

.metric-icon-box {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-blue { background: #0f172a; color: #ffffff; }
.bg-red { background: #b91c1c; color: #ffffff; }
.bg-gold-dark { background: #78350f; color: #ffffff; }

.metric-icon-box svg {
  width: 24px;
  height: 24px;
}

/* Dashboard Grid (2 columns) */
.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 32px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
}

.view-all {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  text-decoration: none;
}

/* Task Inbox */
.task-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  gap: 16px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.task-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.task-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-top: 6px;
  flex-shrink: 0;
}

.task-indicator.red { background: #ef4444; }
.task-indicator.gold { background: #d97706; }
.task-indicator.gray { background: #cbd5e1; }

.task-content {
  flex: 1;
}

.task-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.tag {
  font-size: 10px;
  font-weight: 700;
  padding: 4px 8px;
  border-radius: 4px;
  letter-spacing: 0.05em;
}

.tag-red { background: #fee2e2; color: #b91c1c; }
.tag-gold { background: #fef3c7; color: #b45309; }
.tag-gray { background: #e2e8f0; color: #475569; }

.task-due {
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
}

.task-title {
  font-size: 16px;
  font-weight: 600;
  color: #0f172a;
  margin-bottom: 6px;
}

.task-meta {
  font-size: 13px;
  color: #64748b;
}

.task-actions {
  display: flex;
  gap: 8px;
}

.mt-3 {
  margin-top: 12px;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 600;
  border-radius: 6px;
  cursor: pointer;
  border: none;
  transition: opacity 0.2s;
}

.btn-sm:hover {
  opacity: 0.9;
}

.btn-primary {
  background: #0f172a;
  color: #ffffff;
}

.btn-success {
  background: #059669;
  color: #ffffff;
}

.btn-danger {
  background: #dc2626;
  color: #ffffff;
}

/* Calendar Widget */
.calendar-widget {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.month {
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: #0f172a;
}

.calendar-nav {
  display: flex;
  gap: 8px;
}

.cal-btn {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #64748b;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
  text-align: center;
}

.day-label {
  font-size: 11px;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 8px;
}

.day {
  font-size: 13px;
  font-weight: 500;
  color: #0f172a;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin: 0 auto;
}

.day.muted { color: #cbd5e1; }
.day.active-red { color: #ef4444; font-weight: 700; position: relative; }
.day.active-red::after {
  content: '';
  position: absolute;
  bottom: 0px;
  width: 4px;
  height: 4px;
  background: #ef4444;
  border-radius: 50%;
}
.day.active-dot { position: relative; }
.day.active-dot::after {
  content: '';
  position: absolute;
  bottom: 0px;
  width: 4px;
  height: 4px;
  background: #d97706;
  border-radius: 50%;
}
.day.selected {
  background: #0f172a;
  color: #ffffff;
}

/* System Notifications */
.notifications-list {
  background: #ffffff;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.notification-item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  gap: 16px;
}

.notif-icon {
  width: 20px;
  height: 20px;
  margin-top: 2px;
  flex-shrink: 0;
}

.notif-icon.blue { color: #0ea5e9; }
.notif-icon.gray { color: #64748b; }

.notif-content p {
  font-size: 13px;
  color: #0f172a;
  line-height: 1.5;
  margin-bottom: 8px;
}

.notif-time {
  font-size: 11px;
  color: #94a3b8;
}

/* Modal Overlay & Preview */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(15, 23, 42, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-content.preview-modal {
  background: #ffffff;
  width: 700px;
  max-width: 90vw;
  max-height: 90vh;
  border-radius: 16px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  padding: 24px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f8fafc;
}

.modal-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
}

.modal-body.preview-body {
  padding: 32px 24px;
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  padding: 20px 24px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  background: #f8fafc;
}
</style>
