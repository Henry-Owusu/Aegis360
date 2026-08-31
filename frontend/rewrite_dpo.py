import os

# Files
DASHBOARD_PATH = "/Users/henry/Aegis360/frontend/src/views/dpo/DpoDashboardView.vue"
QUESTIONS_PATH = "/Users/henry/Aegis360/frontend/src/views/dpo/DpoQuestionManagementView.vue"

# 1. Read dashboard styles
with open(DASHBOARD_PATH, 'r') as f:
    dashboard_lines = f.readlines()

style_start = -1
for i, line in enumerate(dashboard_lines):
    if "<style scoped>" in line:
        style_start = i
        break

dashboard_styles = "".join(dashboard_lines[style_start+1:]) # exclude <style scoped> tag

# 2. Define the new component script & template
new_content = """<script setup lang="ts">
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

const isAddingQuestion = ref(false)
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

const handleAddQuestion = async () => {
  if (newQuestion.value.question_text.trim() === '') return
  if (newQuestion.value.question_number.trim() === '') return
  if (newQuestion.value.section_title.trim() === '') return
  
  try {
    const payload = {
      ...newQuestion.value,
      section: activeSectionId.value,
      options: ['Radio', 'Checkbox', 'Dropdown'].includes(newQuestion.value.answer_type) ? newQuestion.value.options : null
    }
    await dpiaApi.createQuestion(payload)
    
    isAddingQuestion.value = false
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
    
    await loadQuestions()
  } catch (error) {
    console.error('Failed to create question', error)
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
          <button class="btn-primary" @click="isAddingQuestion = true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="btn-icon">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            ADD QUESTION
          </button>
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
                  <span class="q-number">{{ q.question_number }}</span>
                  <span class="q-type">{{ q.answer_type }}</span>
                  <span v-if="q.required" class="q-badge required">Required</span>
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
                <h3>Add New Question</h3>
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
                
                <button class="btn-primary full-width mt-4" @click="handleAddQuestion">Save Question</button>
              </div>
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
  gap: 24px;
}

.section-tabs {
  display: flex;
  gap: 8px;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 8px;
}

.tab-btn {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  font-size: 1rem;
  font-weight: 500;
  padding: 8px 16px;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s;
}

.tab-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.tab-btn.active {
  background: var(--primary-color-10);
  color: var(--primary-color);
}

.workspace-grid {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

.questions-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: var(--text-secondary);
  background: var(--bg-card);
  border-radius: 12px;
  border: 1px dashed var(--border-color);
}

.question-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 24px;
  transition: all 0.2s ease;
}

.question-card:hover {
  border-color: var(--primary-color-50);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.q-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.q-number {
  background: var(--bg-hover);
  padding: 4px 8px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.q-type {
  font-size: 0.85rem;
  color: var(--primary-color);
  font-weight: 500;
}

.q-badge {
  font-size: 0.75rem;
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.q-badge.required {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.q-title {
  font-size: 1.1rem;
  font-weight: 500;
  margin: 0 0 8px 0;
  line-height: 1.4;
}

.q-subtitle {
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin: 0 0 8px 0;
}

.q-guidance {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin: 0 0 16px 0;
  font-style: italic;
}

.q-options {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.q-option-pill {
  background: var(--bg-hover);
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.properties-panel {
  width: 340px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 24px;
}

.panel-header {
  padding: 20px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-header h3 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 1.5rem;
  cursor: pointer;
}

.panel-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.form-group input[type="text"],
.form-group input[type="number"],
.form-group select,
.form-group textarea {
  background: var(--bg-dark);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  padding: 10px 12px;
  border-radius: 6px;
  font-family: inherit;
  font-size: 0.95rem;
}

.options-group {
  background: var(--bg-dark);
  padding: 12px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.option-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-card);
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 0.9rem;
}

.btn-icon {
  background: none;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0 4px;
}

.add-option {
  display: flex;
  gap: 8px;
}

.checkbox-group {
  flex-direction: row;
  align-items: center;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: var(--text-primary);
}

.full-width {
  width: 100%;
}
.mt-4 {
  margin-top: 16px;
}

.btn-outline {
  background: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-outline:hover {
  background: var(--bg-hover);
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.85rem;
}

"""

with open(QUESTIONS_PATH, 'w') as f:
    f.write(new_content)
    f.write("<style scoped>\n")
    f.write(dashboard_styles)

print("Updated DpoQuestionManagementView.vue")
