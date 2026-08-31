<script setup lang="ts">
import { ref } from 'vue'
import AdminLayout from './components/AdminLayout.vue'

// ─── Mock Data ────────────────────────────────────────────────────────────────

const questions = ref([
  { id: 'q1', text: 'Does this project involve the processing of sensitive personal data?', module: 'DPIA', type: 'Yes/No', required: true, status: 'active' },
  { id: 'q2', text: 'Are you transferring data outside the EU/EEA?', module: 'DPIA', type: 'Yes/No', required: true, status: 'active' },
  { id: 'q3', text: 'Describe the nature of the data being processed.', module: 'DPIA', type: 'Long Text', required: true, status: 'active' },
  { id: 'q4', text: 'What is the lawful basis for processing?', module: 'DPIA', type: 'Single Select', required: true, status: 'draft' },
  { id: 'q5', text: 'Identify third-party processors involved.', module: 'Vendor Risk', type: 'Multi Select', required: false, status: 'active' }
])

const filterModule = ref('all')
const searchQuery = ref('')
</script>

<template>
  <AdminLayout>
    <div class="page-header">
      <div>
        <h2 class="page-title">Question Bank</h2>
        <p class="page-sub">Manage the master list of questions used across assessments</p>
      </div>
      <button class="btn-primary">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        Add Question
      </button>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <div class="search-box">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input v-model="searchQuery" type="text" placeholder="Search questions..." />
      </div>
      <div class="filters">
        <select v-model="filterModule" class="filter-select">
          <option value="all">All Modules</option>
          <option value="DPIA">DPIA</option>
          <option value="Vendor Risk">Vendor Risk</option>
        </select>
      </div>
    </div>

    <!-- Questions List -->
    <div class="questions-list">
      <div v-for="q in questions" :key="q.id" class="question-card">
        <div class="q-drag-handle">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="9" cy="5" r="1"></circle><circle cx="9" cy="12" r="1"></circle><circle cx="9" cy="19" r="1"></circle>
            <circle cx="15" cy="5" r="1"></circle><circle cx="15" cy="12" r="1"></circle><circle cx="15" cy="19" r="1"></circle>
          </svg>
        </div>
        
        <div class="q-content">
          <div class="q-header">
            <span class="q-module">{{ q.module }}</span>
            <span v-if="q.required" class="q-req">Required</span>
            <span class="q-type">{{ q.type }}</span>
            <span class="q-status" :class="q.status">{{ q.status }}</span>
          </div>
          <p class="q-text">{{ q.text }}</p>
        </div>
        
        <div class="q-actions">
          <button class="icon-btn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg></button>
          <button class="icon-btn danger"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg></button>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<style scoped>
/* ── Page Header ─────────────────────────────────────────────── */
.page-header {
  display: flex; justify-content: space-between; align-items: flex-start;
  margin-bottom: 32px;
}
.page-title {
  font-size: 24px; font-weight: 700; color: #FFFFFF; margin: 0 0 6px;
}
.page-sub {
  color: #92929D; font-size: 14px; margin: 0;
}
.btn-primary {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 20px; border-radius: 12px;
  background: linear-gradient(135deg, #FDBA74, #F58425);
  border: none; color: #FFFFFF;
  font-size: 14px; font-weight: 600; cursor: pointer;
}

/* ── Toolbar ─────────────────────────────────────────────────── */
.toolbar {
  display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap;
}
.search-box {
  flex: 1; min-width: 260px; display: flex; align-items: center; gap: 10px;
  background: #1C1C24; border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px; padding: 0 16px;
}
.search-box svg { width: 18px; height: 18px; color: #92929D; }
.search-box input {
  background: transparent; border: none; color: #FFFFFF; font-size: 14px;
  outline: none; width: 100%; padding: 12px 0;
}
.filters { display: flex; gap: 12px; }
.filter-select {
  background: #1C1C24; border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px; color: #FFFFFF; font-size: 13px;
  padding: 10px 16px; outline: none; cursor: pointer;
}

/* ── Questions List ──────────────────────────────────────────── */
.questions-list {
  display: flex; flex-direction: column; gap: 16px;
}
.question-card {
  background: #1C1C24; border: 1px solid rgba(255,255,255,0.04);
  border-radius: 16px; padding: 20px;
  display: flex; align-items: flex-start; gap: 16px;
  transition: transform 0.2s, border-color 0.2s;
}
.question-card:hover {
  border-color: rgba(255,255,255,0.1);
  transform: translateX(4px);
}
.q-drag-handle {
  color: #4A4A5A; cursor: grab; padding-top: 4px;
}
.q-drag-handle svg { width: 20px; height: 20px; }

.q-content { flex: 1; }
.q-header { display: flex; gap: 8px; margin-bottom: 8px; align-items: center; }
.q-module { font-size: 11px; font-weight: 700; color: #94A3B8; background: rgba(148,163,184,0.1); padding: 4px 8px; border-radius: 6px; }
.q-type { font-size: 11px; color: #92929D; border: 1px solid rgba(255,255,255,0.1); padding: 3px 8px; border-radius: 6px; }
.q-req { font-size: 11px; color: #F58425; font-weight: 600; }
.q-status { font-size: 11px; padding: 3px 8px; border-radius: 6px; font-weight: 600; text-transform: uppercase; margin-left: auto; }
.q-status.active { color: #4ADE80; background: rgba(74,222,128,0.1); }
.q-status.draft { color: #FDBA74; background: rgba(253,186,116,0.1); }

.q-text { font-size: 16px; color: #FFFFFF; font-weight: 500; margin: 0; }

.q-actions {
  display: flex; gap: 8px;
}
.icon-btn {
  background: rgba(255,255,255,0.05); border: none; color: #E2E8F0;
  width: 36px; height: 36px; border-radius: 10px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.2s;
}
.icon-btn:hover { background: rgba(255,255,255,0.1); }
.icon-btn.danger:hover { background: rgba(239,68,68,0.2); color: #F87171; }
.icon-btn svg { width: 16px; height: 16px; }
</style>
