<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AegisLogo from '@/components/common/AegisLogo.vue'

const router = useRouter()

const templates = ref([
  { id: 1, name: 'Initial Screening (PIA)', active: true },
  { id: 2, name: 'Full DPIA Assessment', active: false },
  { id: 3, name: 'Vendor Risk Questionnaire', active: false }
])

const questions = ref([
  { id: 1, text: 'Does this project involve the processing of personal data?', type: 'Yes/No', weight: 'High' },
  { id: 2, text: 'Will data be transferred outside the EU/EEA?', type: 'Yes/No', weight: 'Critical' },
  { id: 3, text: 'What is the primary purpose of the data collection?', type: 'Long Text', weight: 'Medium' }
])

const isAddingQuestion = ref(false)
const newQuestion = ref({ text: '', type: 'Yes/No', weight: 'Low' })

const handleNavigateDashboard = () => {
  router.push('/dpo/dashboard')
}

const handleAddQuestion = () => {
  if (newQuestion.value.text.trim() === '') return
  
  questions.value.push({
    id: Date.now(),
    text: newQuestion.value.text,
    type: newQuestion.value.type,
    weight: newQuestion.value.weight
  })
  
  isAddingQuestion.value = false
  newQuestion.value = { text: '', type: 'Yes/No', weight: 'Low' }
}
</script>

<template>
  <div class="builder-layout">
    <!-- Top Navigation -->
    <header class="top-nav">
      <div class="nav-left">
        <div class="brand" @click="handleNavigateDashboard">
          <AegisLogo :height="42" />
        </div>
        <div class="divider"></div>
        <h1 class="page-title">Template Builder</h1>
      </div>

      <div class="nav-right">
        <button class="btn-outline" @click="handleNavigateDashboard">Cancel</button>
        <button class="btn-primary" @click="handleNavigateDashboard">Save Template</button>
      </div>
    </header>

    <div class="workspace">
      <!-- Templates Sidebar -->
      <aside class="templates-sidebar">
        <div class="sidebar-header">
          <h2>Templates</h2>
          <button class="icon-btn" title="Create New Template">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
          </button>
        </div>

        <div class="template-list">
          <div 
            v-for="template in templates" 
            :key="template.id"
            class="template-item"
            :class="{ active: template.active }"
          >
            <svg class="file-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            <span>{{ template.name }}</span>
          </div>
        </div>
      </aside>

      <!-- Main Builder Area -->
      <main class="builder-content">
        <div class="builder-header">
          <div>
            <h2 class="template-title">Initial Screening (PIA)</h2>
            <p class="template-desc">Manage the standard questions asked during the preliminary risk screening.</p>
          </div>
          <button class="btn-add" @click="isAddingQuestion = true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            Add Question
          </button>
        </div>

        <div class="questions-list">
          <div v-for="(question, index) in questions" :key="question.id" class="question-card">
            <div class="drag-handle">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="8" y1="6" x2="21" y2="6"></line>
                <line x1="8" y1="12" x2="21" y2="12"></line>
                <line x1="8" y1="18" x2="21" y2="18"></line>
                <line x1="3" y1="6" x2="3.01" y2="6"></line>
                <line x1="3" y1="12" x2="3.01" y2="12"></line>
                <line x1="3" y1="18" x2="3.01" y2="18"></line>
              </svg>
            </div>
            <div class="question-details">
              <div class="question-meta">
                <span class="q-number">Q{{ index + 1 }}</span>
                <span class="q-type">{{ question.type }}</span>
                <span class="q-weight" :class="question.weight.toLowerCase()">{{ question.weight }} Risk</span>
              </div>
              <h3 class="q-text">{{ question.text }}</h3>
            </div>
            <div class="question-actions">
              <button class="action-btn" title="Edit">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                  <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                </svg>
              </button>
              <button class="action-btn delete" title="Delete">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="3 6 5 6 21 6"></polyline>
                  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Add Question Form (Modal style inline) -->
        <div v-if="isAddingQuestion" class="add-question-form">
          <h3 class="form-title">New Question</h3>
          
          <div class="form-group">
            <label>Question Text</label>
            <input type="text" v-model="newQuestion.text" placeholder="e.g., Does this application use AI?" />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Response Type</label>
              <select v-model="newQuestion.type">
                <option>Yes/No</option>
                <option>Multiple Choice</option>
                <option>Short Text</option>
                <option>Long Text</option>
              </select>
            </div>

            <div class="form-group">
              <label>Risk Weighting</label>
              <select v-model="newQuestion.weight">
                <option>Low</option>
                <option>Medium</option>
                <option>High</option>
                <option>Critical</option>
              </select>
            </div>
          </div>

          <div class="form-actions">
            <button class="btn-text" @click="isAddingQuestion = false">Cancel</button>
            <button class="btn-primary" @click="handleAddQuestion">Save Question</button>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
.builder-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f8f9fa;
  font-family: 'Inter', system-ui, sans-serif;
  color: #1e293b;
}

/* Top Nav */
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

.nav-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.brand-name {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: 0.02em;
}

.divider {
  width: 1px;
  height: 24px;
  background: #cbd5e1;
}

.page-title {
  font-size: 16px;
  font-weight: 600;
  color: #64748b;
}

.nav-right {
  display: flex;
  gap: 12px;
}

.btn-outline {
  padding: 8px 16px;
  border: 1px solid #cbd5e1;
  background: transparent;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
}

.btn-primary {
  padding: 8px 16px;
  background: #0f172a;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 600;
  color: #ffffff;
  cursor: pointer;
}

.btn-primary:hover {
  background: #1e293b;
}

/* Workspace */
.workspace {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* Sidebar */
.templates-sidebar {
  width: 280px;
  background: #ffffff;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sidebar-header h2 {
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.icon-btn {
  background: transparent;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 4px;
}

.icon-btn svg {
  width: 18px;
  height: 18px;
}

.template-list {
  display: flex;
  flex-direction: column;
  padding: 0 16px;
  gap: 4px;
}

.template-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}

.template-item:hover {
  background: #f1f5f9;
}

.template-item.active {
  background: #eff6ff;
  color: #1d4ed8;
  font-weight: 600;
}

.file-icon {
  width: 18px;
  height: 18px;
}

/* Main Builder */
.builder-content {
  flex: 1;
  padding: 40px;
  overflow-y: auto;
  max-width: 900px;
  margin: 0 auto;
}

.builder-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.template-title {
  font-size: 24px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 8px;
}

.template-desc {
  font-size: 14px;
  color: #64748b;
}

.btn-add {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  color: #0f172a;
  cursor: pointer;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

.btn-add:hover {
  background: #f8fafc;
}

.btn-add svg {
  width: 16px;
  height: 16px;
}

/* Questions List */
.questions-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.question-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: flex-start;
  gap: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.drag-handle {
  color: #cbd5e1;
  cursor: grab;
  margin-top: 2px;
}

.drag-handle svg {
  width: 20px;
  height: 20px;
}

.question-details {
  flex: 1;
}

.question-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.q-number {
  font-size: 12px;
  font-weight: 700;
  color: #475569;
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
}

.q-type {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
}

.q-weight {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 12px;
  text-transform: uppercase;
}

.q-weight.high { background: #fee2e2; color: #b91c1c; }
.q-weight.critical { background: #7f1d1d; color: #ffffff; }
.q-weight.medium { background: #fef3c7; color: #b45309; }
.q-weight.low { background: #f1f5f9; color: #475569; }

.q-text {
  font-size: 16px;
  font-weight: 500;
  color: #0f172a;
}

.question-actions {
  display: flex;
  gap: 8px;
}

.action-btn {
  background: transparent;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 6px;
  border-radius: 6px;
}

.action-btn:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.action-btn.delete:hover {
  background: #fee2e2;
  color: #ef4444;
}

.action-btn svg {
  width: 18px;
  height: 18px;
}

/* Add Question Form */
.add-question-form {
  margin-top: 24px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}

.form-title {
  font-size: 16px;
  font-weight: 600;
  color: #0f172a;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  margin-bottom: 8px;
}

.form-group input,
.form-group select {
  width: 100%;
  height: 40px;
  padding: 0 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-size: 14px;
  color: #0f172a;
  outline: none;
}

.form-group input:focus,
.form-group select:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.btn-text {
  background: transparent;
  border: none;
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  padding: 8px 16px;
}

.btn-text:hover {
  color: #0f172a;
}
</style>
