<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import DpoSidebar from './components/DpoSidebar.vue'
import { dpiaApi, type AssessmentSummary } from '@/services/api'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const assessmentId = route.params.id as string
const assessment = ref<AssessmentSummary | null>(null)
const isLoading = ref(true)

// Data fetching
const allQuestions = ref<any[]>([])
const allResponses = ref<Record<string, any>>({})

const comments = ref('')
const isSubmitting = ref(false)

const loadData = async () => {
  try {
    const [assmtRes, questionsRes, responsesRes] = await Promise.all([
      dpiaApi.getAssessment(assessmentId),
      dpiaApi.getQuestions(),
      dpiaApi.getResponses(assessmentId)
    ])
    
    assessment.value = ('assessment' in assmtRes) ? (assmtRes as any).assessment : assmtRes
    allQuestions.value = questionsRes.questions.filter((q: any) => q.section !== 'full_pia')
    allResponses.value = responsesRes.responses
  } catch (err) {
    console.error('Failed to load assessment data', err)
    window.alert('Failed to load assessment.')
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadData()
})

// Organize questions into sections for the reader
const sections = computed(() => {
  const map: Record<string, any[]> = {}
  allQuestions.value.forEach(q => {
    if (!map[q.section]) {
      map[q.section] = []
    }
    map[q.section].push(q)
  })
  return Object.keys(map).map(secName => ({
    title: map[secName][0].section_title,
    questions: map[secName]
  }))
})

// UX Enhancements: Accordions and Gamified Tracking
const collapsedSections = ref<Set<number>>(new Set())
const reviewedSections = ref<Set<number>>(new Set())

const toggleAccordion = (idx: number) => {
  const newSet = new Set(collapsedSections.value)
  if (newSet.has(idx)) {
    newSet.delete(idx)
  } else {
    newSet.add(idx)
  }
  collapsedSections.value = newSet
}

const toggleSectionReview = (idx: number) => {
  const newSet = new Set(reviewedSections.value)
  if (newSet.has(idx)) {
    newSet.delete(idx)
  } else {
    newSet.add(idx)
    // Auto-collapse when marked as reviewed
    collapsedSections.value = new Set(collapsedSections.value).add(idx)
  }
  reviewedSections.value = newSet
}

// Matrix Grouping & Toggling
const collapsedMatrixGroups = ref<Set<string>>(new Set())

const groupMatrixKeys = (responseObj: Record<string, any>) => {
  const grouped: Record<string, Record<string, any>> = {
    'Personal Data': {},
    'Sensitive Personal Data': {},
    'Other': {}
  }
  
  for (const [key, val] of Object.entries(responseObj)) {
    if (key.startsWith('Personal Data:')) {
      grouped['Personal Data'][key.replace('Personal Data: ', '')] = val
    } else if (key.startsWith('Sensitive Personal Data:')) {
      grouped['Sensitive Personal Data'][key.replace('Sensitive Personal Data: ', '')] = val
    } else {
      grouped['Other'][key] = val
    }
  }
  
  // Clean up empty groups
  const result: Record<string, Record<string, any>> = {}
  for (const [gKey, gVal] of Object.entries(grouped)) {
    if (Object.keys(gVal).length > 0) {
      result[gKey] = gVal
    }
  }
  return result
}

const toggleMatrixGroup = (qId: number, groupName: string) => {
  const key = `${qId}-${groupName}`
  const newSet = new Set(collapsedMatrixGroups.value)
  if (newSet.has(key)) {
    newSet.delete(key)
  } else {
    newSet.add(key)
  }
  collapsedMatrixGroups.value = newSet
}

const isMatrixGroupCollapsed = (qId: number, groupName: string) => {
  // By default, let's have them collapsed to save space!
  // Wait, if it's in the set, it means toggled. 
  // Let's invert: if it's NOT in the set, it's collapsed by default.
  // Actually, Set tracks what is EXPANDED to keep it simple, or Set tracks what is COLLAPSED.
  // Let's have Set track COLLAPSED. Default is open for now, or default is closed?
  // User asked to "collapse ... and make them expandable", which implies default is collapsed.
  // So Set tracks what is EXPANDED.
  return !collapsedMatrixGroups.value.has(`${qId}-${groupName}`)
}

// Two-step approval flow
const showFullPiaPrompt = ref(false)

const handleApprove = () => {
  // Step 1: Approved — now ask about Full PIA
  showFullPiaPrompt.value = true
}

const handleReturn = async () => {
  if (isSubmitting.value) return
  isSubmitting.value = true
  try {
    await dpiaApi.reviewAssessment(assessmentId, {
      action: 'Return',
      comments: comments.value
    })
    window.alert('Assessment returned for mitigation.')
    router.push('/dpo/dashboard')
  } catch (err) {
    console.error('Error returning assessment:', err)
    window.alert('Failed to submit review.')
  } finally {
    isSubmitting.value = false
  }
}

const handleReviewAction = async (actionType: string) => {
  if (isSubmitting.value) return
  isSubmitting.value = true
  try {
    await dpiaApi.reviewAssessment(assessmentId, {
      action: actionType,
      comments: comments.value
    })
    
    if (actionType === 'Require Full PIA') {
      // Smooth UX: Transition immediately to completing the Full PIA
      router.push(`/dpo/dpia/${assessmentId}/full`)
      return
    }

    window.alert(`Assessment successfully marked as ${actionType}!`)
    router.push('/dpo/dashboard')
  } catch (err) {
    console.error('Error reviewing assessment:', err)
    window.alert('Failed to submit review.')
  } finally {
    isSubmitting.value = false
  }
}

const handleNavigateDashboard = () => {
  router.push('/dpo/dashboard')
}
</script>

<template>
  <div class="review-layout">
    <DpoSidebar />

    <main class="main-workspace" v-if="!isLoading && assessment">
      <!-- Top Action Bar -->
      <header class="workspace-header">
        <div class="header-left">
          <button class="btn-back" @click="handleNavigateDashboard">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="19" y1="12" x2="5" y2="12"></line>
              <polyline points="12 19 5 12 12 5"></polyline>
            </svg>
            Back to Dashboard
          </button>
          <div class="header-title-box">
            <h1>{{ assessment.title }}</h1>
            <span class="status-badge">{{ assessment.status }}</span>
          </div>
        </div>
      </header>

      <!-- Split Layout -->
      <div class="split-layout">
        
        <!-- Left Panel: Document Reader -->
        <div class="reader-panel">
          <div class="reader-container">
            
            <!-- Table of Contents Sidebar -->
            <aside class="toc-sidebar fade-in">
              <h4 class="toc-title">Document Outline</h4>
              <nav class="toc-nav">
                <a 
                  v-for="(sec, idx) in sections" 
                  :key="idx" 
                  :href="'#section-' + idx"
                  class="toc-link"
                  :class="{ 'reviewed': reviewedSections.has(idx) }"
                >
                  <div class="toc-link-content">
                    <span class="toc-text">{{ sec.title }}</span>
                    <span v-if="reviewedSections.has(idx)" class="toc-check">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                        <polyline points="20 6 9 17 4 12"></polyline>
                      </svg>
                    </span>
                  </div>
                </a>
              </nav>
              
              <div class="toc-progress">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: (reviewedSections.size / sections.length * 100) + '%' }"></div>
                </div>
                <span class="progress-text">{{ reviewedSections.size }} of {{ sections.length }} sections reviewed</span>
              </div>
            </aside>

            <!-- Main Content -->
            <div class="reader-content fade-in">
              <div class="document-cover">
                <div class="cover-bg"></div>
                <div class="cover-content">
                  <h2 class="doc-title">DPIA Submission Document</h2>
                  <div class="doc-meta-pills">
                    <span class="meta-pill">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
                      {{ assessment.project_manager }}
                    </span>
                    <span class="meta-pill">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                      {{ new Date(assessment.created_at).toLocaleDateString() }}
                    </span>
                  </div>
                </div>
              </div>
              
              <div v-for="(sec, idx) in sections" :key="idx" :id="'section-' + idx" class="doc-section">
                <!-- Accordion Header -->
                <div class="section-header-bar" @click="toggleAccordion(idx)">
                  <h3 class="sec-title">{{ sec.title }}</h3>
                  <div class="header-right">
                    <span v-if="reviewedSections.has(idx)" class="status-reviewed">Reviewed</span>
                    <svg :class="{'rotated': !collapsedSections.has(idx)}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="chevron-icon">
                      <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                  </div>
                </div>
                
                <!-- Accordion Content -->
                <div v-show="!collapsedSections.has(idx)" class="q-a-list">
                  <div v-for="q in sec.questions" :key="q.id" class="q-a-item">
                    <div class="q-text">
                      <span class="q-num">{{ q.question_number || '•' }}</span>
                      {{ q.question_text }}
                    </div>
                    <div class="a-text">
                      <span v-if="allResponses[q.id]" :class="['a-value', {'warning-value': allResponses[q.id] === 'Yes'}]">
                        <template v-if="Array.isArray(allResponses[q.id])">
                          <ul class="a-list">
                            <li v-for="ans in allResponses[q.id]" :key="ans">{{ ans }}</li>
                          </ul>
                        </template>
                        <template v-else-if="typeof allResponses[q.id] === 'object' && allResponses[q.id] !== null">
                          <div class="matrix-response">
                            <div 
                              v-for="(group, groupName) in groupMatrixKeys(allResponses[q.id])" 
                              :key="groupName" 
                              class="matrix-group"
                            >
                              <div class="matrix-group-header" @click="toggleMatrixGroup(q.id, groupName as string)">
                                <span class="matrix-group-title">{{ groupName }}</span>
                                <svg :class="{'rotated': !isMatrixGroupCollapsed(q.id, groupName as string)}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="chevron-icon">
                                  <polyline points="6 9 12 15 18 9"></polyline>
                                </svg>
                              </div>
                              <div v-show="!isMatrixGroupCollapsed(q.id, groupName as string)" class="matrix-group-content">
                                <div v-for="(val, key) in group" :key="key" class="matrix-row">
                                  <span class="matrix-key">{{ key }}</span>
                                  <span class="matrix-val">
                                    <template v-if="Array.isArray(val) && val.length > 0">
                                      <span class="badge" v-for="item in val" :key="item">{{ item }}</span>
                                    </template>
                                    <template v-else-if="Array.isArray(val) && val.length === 0">
                                      <span class="muted-text">None selected</span>
                                    </template>
                                    <template v-else>
                                      {{ val }}
                                    </template>
                                  </span>
                                </div>
                              </div>
                            </div>
                          </div>
                        </template>
                        <template v-else>{{ allResponses[q.id] }}</template>
                      </span>
                      <span v-else class="a-empty">No response provided.</span>
                    </div>
                  </div>
                  
                  <!-- Section Footer (Mark as Reviewed) -->
                  <div class="section-footer">
                    <button 
                      :class="['btn-review-toggle', { 'is-reviewed': reviewedSections.has(idx) }]"
                      @click="toggleSectionReview(idx)"
                    >
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <polyline points="20 6 9 17 4 12"></polyline>
                      </svg>
                      {{ reviewedSections.has(idx) ? 'Reviewed' : 'Mark as Reviewed' }}
                    </button>
                  </div>
                </div>
              </div>
              
            </div>
          </div>
        </div>

        <!-- Right Panel: Action Center -->
        <div class="action-panel">
          <div class="action-card fade-in-up">
            <h3>DPO Review Decision</h3>
            <p class="action-desc">Review the submission and provide your official decision.</p>
            
            <div class="comment-box">
              <label>Review Comments / Feedback</label>
              <textarea 
                v-model="comments" 
                rows="4" 
                placeholder="Enter feedback for the Project Manager..."
              ></textarea>
            </div>
            
            <div class="action-buttons">

              <!-- If status is already Requires Full PIA -->
              <template v-if="assessment.status === 'Requires Full PIA'">
                <button 
                  class="btn-action btn-full-pia" 
                  @click="router.push(`/dpo/dpia/${assessment.id}/full`)"
                >
                  <div class="icon-circle">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                      <polyline points="14 2 14 8 20 8"></polyline>
                      <line x1="16" y1="13" x2="8" y2="13"></line>
                      <line x1="16" y1="17" x2="8" y2="17"></line>
                      <polyline points="10 9 9 9 8 9"></polyline>
                    </svg>
                  </div>
                  <div class="btn-text">
                    <span>Complete Full PIA</span>
                    <small>Fill out detailed assessment</small>
                  </div>
                </button>
              </template>

              <!-- Step 1: Main decision (shown by default) -->
              <template v-else-if="!showFullPiaPrompt">
                <button 
                  class="btn-action btn-approve" 
                  @click="handleApprove"
                  :disabled="isSubmitting"
                >
                  <div class="icon-circle">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <polyline points="20 6 9 17 4 12"></polyline>
                    </svg>
                  </div>
                  <div class="btn-text">
                    <span>Approve DPIA</span>
                    <small>Proceed to next step</small>
                  </div>
                </button>
                
                <button 
                  class="btn-action btn-return" 
                  @click="handleReturn"
                  :disabled="isSubmitting"
                >
                  <div class="icon-circle">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                      <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
                      <path d="M3 3v5h5"></path>
                    </svg>
                  </div>
                  <div class="btn-text">
                    <span>Return for Mitigation</span>
                    <small>Send back for fixes</small>
                  </div>
                </button>
              </template>

              <!-- Step 2: Full PIA decision (shown after Approve) -->
              <template v-else>
                <div class="full-pia-prompt">
                  <div class="full-pia-header">
                    <div class="full-pia-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="20 6 9 17 4 12"></polyline>
                      </svg>
                    </div>
                    <div>
                      <p class="full-pia-title">DPIA Approved</p>
                      <p class="full-pia-sub">Does this assessment require a Full PIA?</p>
                    </div>
                  </div>

                  <button
                    class="btn-action btn-full-pia"
                    @click="handleReviewAction('Require Full PIA')"
                    :disabled="isSubmitting"
                  >
                    <div class="icon-circle">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <circle cx="12" cy="12" r="10"></circle>
                        <line x1="12" y1="8" x2="12" y2="12"></line>
                        <line x1="12" y1="16" x2="12.01" y2="16"></line>
                      </svg>
                    </div>
                    <div class="btn-text">
                      <span>Yes – Require Full PIA</span>
                      <small>Escalate to full risk assessment</small>
                    </div>
                  </button>

                  <button
                    class="btn-action btn-approve"
                    @click="handleReviewAction('Approve')"
                    :disabled="isSubmitting"
                  >
                    <div class="icon-circle">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <polyline points="20 6 9 17 4 12"></polyline>
                      </svg>
                    </div>
                    <div class="btn-text">
                      <span>No – Approve &amp; Close</span>
                      <small>No further action required</small>
                    </div>
                  </button>

                  <button class="btn-back-step" @click="showFullPiaPrompt = false">
                    ← Back to decisions
                  </button>
                </div>
              </template>

            </div>
            
          </div>
        </div>
      </div>
    </main>
    
    <div v-else class="loading-state">
      Loading assessment details...
    </div>
  </div>
</template>

<style scoped>
.review-layout {
  display: flex;
  height: 100vh;
  background-color: #f8fafc;
  overflow: hidden;
}

.main-workspace {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.workspace-header {
  height: 80px;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  padding: 0 40px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.02);
  z-index: 10;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  color: #64748b;
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: color 0.2s;
}

.btn-back:hover {
  color: #0f172a;
}

.btn-back svg {
  width: 18px;
  height: 18px;
}

.header-title-box {
  display: flex;
  align-items: center;
  gap: 16px;
  border-left: 2px solid #e2e8f0;
  padding-left: 24px;
}

.header-title-box h1 {
  font-size: 20px;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.status-badge {
  background: #e0f2fe;
  color: #0369a1;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Split Layout */
.split-layout {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* Left Panel: Document Reader */
.reader-panel {
  flex: 1;
  overflow-y: auto;
  padding: 40px;
  display: flex;
  justify-content: center;
}

.reader-container {
  display: flex;
  gap: 32px;
  width: 100%;
  max-width: 1100px;
}

.toc-sidebar {
  width: 250px;
  flex-shrink: 0;
  position: sticky;
  top: 0;
  align-self: flex-start;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(15, 23, 42, 0.04);
  border: 1px solid #f1f5f9;
  padding: 24px;
}

.toc-title {
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 16px;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 8px;
}

.toc-nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.toc-link {
  text-decoration: none;
  font-size: 13.5px;
  color: #64748b;
  font-weight: 500;
  padding: 8px 12px;
  border-radius: 8px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.toc-link:hover {
  background: #f8fafc;
  color: #0f172a;
}

.toc-link.reviewed {
  color: #F58425;
}

.toc-link-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.toc-check {
  color: #22c55e;
}

.toc-check svg {
  width: 16px;
  height: 16px;
}

.toc-progress {
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.progress-bar {
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: #22c55e;
  transition: width 0.3s;
}

.progress-text {
  font-size: 12px;
  color: #64748b;
}

.reader-content {
  background: #ffffff;
  flex: 1;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(15, 23, 42, 0.04);
  border: 1px solid #f1f5f9;
  padding: 48px;
  min-height: 100%;
}

.document-cover {
  position: relative;
  overflow: hidden;
  border-radius: 12px;
  margin-bottom: 40px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}

.cover-bg {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: #fff7ed;
  z-index: 0;
}

.cover-content {
  position: relative;
  z-index: 1;
  padding: 40px;
}

.doc-title {
  font-size: 28px;
  font-weight: 800;
  color: #0f172a;
  margin: 0 0 24px 0;
  letter-spacing: -0.5px;
}

.doc-meta-pills {
  display: flex;
  gap: 16px;
}

.meta-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #ffffff;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 13.5px;
  font-weight: 600;
  color: #334155;
  border: 1px solid #e2e8f0;
}

.meta-pill svg {
  width: 16px;
  height: 16px;
  color: #F58425;
}

.doc-section {
  background: #ffffff;
  border: 1px solid #f1f5f9;
  border-radius: 12px;
  padding: 32px;
  margin-bottom: 32px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
}

.section-header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  padding-bottom: 16px;
  margin-bottom: 24px;
  border-bottom: 1px solid #f1f5f9;
  transition: all 0.2s;
}

.section-header-bar:hover .sec-title {
  color: #4f46e5;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-reviewed {
  font-size: 11px;
  font-weight: 800;
  color: #166534;
  background: #f0fdf4;
  padding: 5px 12px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border: 1px solid #86efac;
}

.chevron-icon {
  width: 20px;
  height: 20px;
  color: #94a3b8;
  transition: transform 0.2s;
}

.chevron-icon.rotated {
  transform: rotate(180deg);
}

.sec-title {
  font-size: 15px;
  font-weight: 700;
  color: #334155;
  text-transform: uppercase;
  letter-spacing: 1.2px;
}

.section-header-bar:hover .sec-title {
  color: #4f46e5;
}

.q-a-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.q-a-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.q-text {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.5;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.q-num {
  color: #F58425;
  font-weight: 800;
  background: #fff7ed;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 13px;
  flex-shrink: 0;
}

.a-text {
  padding-left: 40px;
}

.a-value {
  font-size: 15px;
  color: #334155;
  background: #f8fafc;
  padding: 16px 20px;
  border-radius: 12px;
  display: inline-block;
  width: 100%;
  border: 1px solid #e2e8f0;
  border-left: 4px solid #F58425;
}

.a-list {
  margin: 0;
  padding-left: 20px;
}

.a-list li {
  margin-bottom: 4px;
}

.matrix-response {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}

.matrix-group {
  display: flex;
  flex-direction: column;
  background: #fff7ed;
  border: 1px solid #fed7aa;
  border-radius: 10px;
  overflow: hidden;
  transition: box-shadow 0.2s;
}

.matrix-group:hover {
  box-shadow: 0 4px 16px rgba(245, 132, 37, 0.08);
}

.matrix-group-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  background: #fff7ed;
  cursor: pointer;
  transition: background 0.2s;
}

.matrix-group-header:hover {
  background: #fed7aa;
}

.matrix-group-title {
  font-weight: 700;
  color: #F58425;
  font-size: 14px;
  letter-spacing: 0.3px;
}

.matrix-group-content {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  border-top: 1px solid #e2e8f0;
}

.matrix-row {
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  overflow: hidden;
}

.matrix-key {
  font-weight: 600;
  color: #334155;
  background: #f8fafc;
  padding: 8px 12px;
  border-bottom: 1px solid #e2e8f0;
  font-size: 14px;
}

.matrix-val {
  padding: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  background: #ffffff;
}

.badge {
  background: #fff7ed;
  color: #F58425;
  padding: 5px 12px;
  border-radius: 20px;
  font-size: 12.5px;
  font-weight: 600;
  border: 1px solid #fed7aa;
  letter-spacing: 0.2px;
}

.muted-text {
  color: #94a3b8;
  font-style: italic;
  font-size: 13px;
}

.a-empty {
  font-size: 14px;
  color: #94a3b8;
  font-style: italic;
}

.section-footer {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px dashed #fed7aa;
  display: flex;
  justify-content: flex-end;
}

.btn-review-toggle {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #fff7ed;
  border: 1.5px solid #fed7aa;
  color: #F58425;
  padding: 10px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.25s;
  letter-spacing: 0.2px;
}

.btn-review-toggle:hover {
  background: #fff7ed;
  border-color: #F58425;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(245, 132, 37, 0.1);
}

.btn-review-toggle.is-reviewed {
  background: #f0fdf4;
  border-color: #22c55e;
  color: #166534;
  box-shadow: 0 2px 8px rgba(34, 197, 94, 0.1);
}

.btn-review-toggle svg {
  width: 18px;
  height: 18px;
}

/* Right Panel: Action Center */
.action-panel {
  width: 400px;
  background: #f1f5f9;
  border-left: 1px solid #e2e8f0;
  padding: 40px 24px;
  overflow-y: auto;
}

.action-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  border: 1px solid #ffffff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
}

.action-card h3 {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 8px 0;
}

.action-desc {
  font-size: 14px;
  color: #64748b;
  margin: 0 0 24px 0;
}

.comment-box {
  margin-bottom: 24px;
}

.comment-box label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  margin-bottom: 8px;
}

.comment-box textarea {
  width: 100%;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 12px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  background: #ffffff;
  transition: all 0.2s;
}

.comment-box textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.btn-action {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
  padding: 16px;
  border-radius: 12px;
  border: 1.5px solid transparent;
  background: #ffffff;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}

.btn-action:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.06);
}

.btn-action:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.icon-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
}

.icon-circle svg {
  width: 20px;
  height: 20px;
}

.btn-text {
  display: flex;
  flex-direction: column;
}

.btn-text span {
  font-size: 15px;
  font-weight: 700;
  color: #0f172a;
}

.btn-text small {
  font-size: 12px;
  color: #64748b;
  margin-top: 2px;
}

/* Specific Action Styles */
.btn-approve:hover:not(:disabled) {
  border-color: #22c55e;
  background: #f0fdf4;
}
.btn-approve:hover .icon-circle {
  background: #22c55e;
  color: #ffffff;
}

.btn-return:hover:not(:disabled) {
  border-color: #f59e0b;
  background: #fffbeb;
}
.btn-return:hover .icon-circle {
  background: #f59e0b;
  color: #ffffff;
}

.btn-full-pia:hover:not(:disabled) {
  border-color: #ef4444;
  background: #fef2f2;
}
.btn-full-pia:hover .icon-circle {
  background: #ef4444;
  color: #ffffff;
}

/* Full PIA Prompt (Step 2) */
.full-pia-prompt {
  display: flex;
  flex-direction: column;
  gap: 12px;
  animation: fadeInUp 0.25s ease-out forwards;
}

.full-pia-header {
  display: flex;
  align-items: center;
  gap: 14px;
  background: #f0fdf4;
  border: 1px solid #86efac;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 4px;
}

.full-pia-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #22c55e;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.full-pia-icon svg {
  width: 18px;
  height: 18px;
}

.full-pia-title {
  font-size: 14px;
  font-weight: 800;
  color: #166534;
  margin: 0 0 2px 0;
}

.full-pia-sub {
  font-size: 13px;
  color: #475569;
  margin: 0;
}

.btn-back-step {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  text-align: left;
  padding: 4px 0;
  transition: color 0.2s;
}

.btn-back-step:hover {
  color: #475569;
}


/* Animations */
.fade-in { animation: fadeIn 0.4s ease-out forwards; }
.fade-in-up { animation: fadeInUp 0.4s ease-out forwards; }

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.loading-state {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  font-size: 16px;
  color: #64748b;
}
</style>
