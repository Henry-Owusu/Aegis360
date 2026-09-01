<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AegisLogo from '@/components/common/AegisLogo.vue'
import DpoSidebar from './components/DpoSidebar.vue'
import { dpiaApi, type AssessmentSummary } from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const assessments = ref<AssessmentSummary[]>([])

const loadAssessments = async () => {
  try {
    const res = await dpiaApi.listAssessments()
    assessments.value = res.assessments
  } catch (err) {
    console.error('Failed to load assessments', err)
  }
}

onMounted(() => {
  loadAssessments()
})

const assignedDpiasCount = computed(
  () => assessments.value.filter((a) => a.status !== 'Draft').length,
)
const riskAnalysisReqdCount = computed(
  () => assessments.value.filter((a) => a.status === 'Submitted').length,
)
const returnedCount = computed(
  () => assessments.value.filter((a) => a.status === 'Returned').length,
)

const priorityQueue = computed(() => {
  return assessments.value
    .filter((a) => ['Submitted', 'Under Review'].includes(a.status))
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 3)
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const handleNavigateManageQuestions = () => {
  router.push('/dpo/questions')
}

const handleNavigateModules = () => {
  router.push('/modules')
}
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
          <svg
            class="search-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
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
              <span class="user-role">{{ authStore.user.role }}</span>
            </div>
            <img :src="authStore.user.avatar" alt="Profile" class="avatar" />
          </div>
        </div>
      </header>

      <div class="dashboard-scroll-area">
        <!-- Dashboard Header -->
        <div class="dashboard-header">
          <div>
            <h1 class="page-title">Data Protection Supervisor</h1>
            <p class="page-subtitle">Your active assessments and risk mitigation tasks.</p>
          </div>
          <button class="btn-primary" @click="handleNavigateManageQuestions">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              class="btn-icon"
            >
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            MANAGE QUESTIONS
          </button>
        </div>

        <!-- Metrics Cards -->
        <div class="metrics-row">
          <div class="metric-card bg-light">
            <div class="metric-content">
              <span class="metric-label">ASSIGNED DPIAS</span>
              <span class="metric-value">{{ assignedDpiasCount }}</span>
            </div>
            <div class="metric-icon-box bg-blue">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
                <polyline points="10 9 9 9 8 9"></polyline>
              </svg>
            </div>
          </div>

          <div class="metric-card bg-red-light">
            <div class="metric-content">
              <span class="metric-label text-red">RISK ANALYSIS REQD</span>
              <div class="value-row">
                <span class="metric-value text-red">{{ riskAnalysisReqdCount }}</span>
                <span v-if="riskAnalysisReqdCount > 0" class="trend up text-red">↑</span>
              </div>
            </div>
            <div class="metric-icon-box bg-red">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path
                  d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"
                ></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
              </svg>
            </div>
          </div>

          <div class="metric-card bg-gold">
            <div class="metric-content">
              <span class="metric-label text-gold-dark">RETURNED BY DPO</span>
              <span class="metric-value text-gold-dark">{{ returnedCount }}</span>
            </div>
            <div class="metric-icon-box bg-gold-dark">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path>
                <path d="M3 3v5h5"></path>
              </svg>
            </div>
          </div>
        </div>

        <div class="dashboard-grid">
          <!-- Main Column -->
          <div class="main-column">
            <div class="section-header">
              <h2 class="section-title">Priority Approval Queue</h2>
              <a href="#" class="view-all">View All →</a>
            </div>

            <div class="task-list">
              <div
                v-if="priorityQueue.length === 0"
                style="padding: 24px; color: #64748b; font-size: 14px"
              >
                No pending assessments in queue.
              </div>
              <div v-for="task in priorityQueue" :key="task.id" class="task-item">
                <div
                  class="task-indicator"
                  :class="task.status === 'Submitted' ? 'red' : 'gold'"
                ></div>
                <div class="task-content">
                  <div class="task-top">
                    <span class="tag" :class="task.status === 'Submitted' ? 'tag-red' : 'tag-gold'">
                      {{ task.status === 'Submitted' ? 'NEW SUBMISSION' : 'UNDER REVIEW' }}
                    </span>
                    <span class="task-due">{{
                      new Date(task.created_at).toLocaleDateString()
                    }}</span>
                  </div>
                  <h4 class="task-title">{{ task.title }}</h4>
                  <p class="task-meta">Initiator: {{ task.project_manager }}</p>
                  <div class="task-actions mt-3">
                    <button class="btn-sm btn-primary">Review</button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Side Column -->
          <div class="side-column">
            <div class="section-header">
              <h2 class="section-title">Upcoming Deadlines</h2>
            </div>
            <div class="calendar-widget">
              <div class="calendar-header">
                <span class="month">OCTOBER</span>
                <div class="calendar-nav">
                  <button class="cal-btn">&lt;</button>
                  <button class="cal-btn">&gt;</button>
                </div>
              </div>
              <div class="calendar-grid">
                <div class="day-label">M</div>
                <div class="day-label">T</div>
                <div class="day-label">W</div>
                <div class="day-label">T</div>
                <div class="day-label">F</div>
                <div class="day-label">S</div>
                <div class="day-label">S</div>

                <div class="day muted">28</div>
                <div class="day muted">29</div>
                <div class="day muted">30</div>
                <div class="day active-red">1</div>
                <div class="day">2</div>
                <div class="day muted">3</div>
                <div class="day muted">4</div>

                <div class="day">5</div>
                <div class="day">6</div>
                <div class="day active-dot">7</div>
                <div class="day selected">8</div>
                <div class="day">9</div>
                <div class="day muted">10</div>
                <div class="day muted">11</div>
              </div>
            </div>

            <div class="section-header" style="margin-top: 32px">
              <h2 class="section-title">System Notifications</h2>
            </div>
            <div class="notifications-list">
              <div class="notification-item">
                <div class="notif-icon blue">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                  </svg>
                </div>
                <div class="notif-content">
                  <p>
                    New regulatory update: EU AI Act guidelines published. Review impact on active
                    AI assessments.
                  </p>
                  <span class="notif-time">2 hours ago</span>
                </div>
              </div>

              <div class="notification-item">
                <div class="notif-icon gray">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="16" x2="12" y2="12"></line>
                    <line x1="12" y1="8" x2="12.01" y2="8"></line>
                  </svg>
                </div>
                <div class="notif-content">
                  <p>Weekly risk report generated successfully.</p>
                  <span class="notif-time">Yesterday</span>
                </div>
              </div>
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

.bg-light {
  background: #f1f5f9;
}
.bg-red-light {
  background: #fee2e2;
}
.bg-gold {
  background: #d97706;
  color: #ffffff;
}

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

.text-red {
  color: #b91c1c;
}
.text-gold-dark {
  color: #ffffff;
}

.metric-icon-box {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-blue {
  background: #0f172a;
  color: #ffffff;
}
.bg-red {
  background: #b91c1c;
  color: #ffffff;
}
.bg-gold-dark {
  background: #78350f;
  color: #ffffff;
}

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
  transition:
    transform 0.2s,
    box-shadow 0.2s;
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

.task-indicator.red {
  background: #ef4444;
}
.task-indicator.gold {
  background: #d97706;
}
.task-indicator.gray {
  background: #cbd5e1;
}

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

.tag-red {
  background: #fee2e2;
  color: #b91c1c;
}
.tag-gold {
  background: #fef3c7;
  color: #b45309;
}
.tag-gray {
  background: #e2e8f0;
  color: #475569;
}

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

.day.muted {
  color: #cbd5e1;
}
.day.active-red {
  color: #ef4444;
  font-weight: 700;
  position: relative;
}
.day.active-red::after {
  content: '';
  position: absolute;
  bottom: 0px;
  width: 4px;
  height: 4px;
  background: #ef4444;
  border-radius: 50%;
}
.day.active-dot {
  position: relative;
}
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

.notif-icon.blue {
  color: #0ea5e9;
}
.notif-icon.gray {
  color: #64748b;
}

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
</style>
