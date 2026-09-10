<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
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
  () => assessments.value.filter((a) => ['Submitted', 'Requires Full PIA'].includes(a.status)).length,
)
const returnedCount = computed(
  () => assessments.value.filter((a) => a.status === 'Returned').length,
)
const fullPiasCompletedCount = computed(
  () => assessments.value.filter((a) => a.status === 'Full PIA Completed').length,
)

const priorityQueue = computed(() => {
  return assessments.value
    .filter((a) => ['Submitted', 'Under Review', 'Requires Full PIA'].includes(a.status))
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 4)
})

const averageTurnaroundTime = computed(() => {
  const completed = assessments.value.filter(a => a.status === 'Full PIA Completed')
  if (completed.length === 0) return 0
  
  const totalDays = completed.reduce((sum, a) => {
    const start = new Date(a.created_at).getTime()
    const end = new Date(a.updated_at).getTime()
    return sum + (end - start) / (1000 * 3600 * 24)
  }, 0)
  
  return Math.round(totalDays / completed.length)
})

const highRiskAssessments = computed(() => {
  const sensitiveKeywords = ['ai', 'biometric', 'health', 'analytics', 'machine learning', 'medical']
  return assessments.value
    .filter(a => ['Submitted', 'Under Review', 'Requires Full PIA'].includes(a.status))
    .filter(a => sensitiveKeywords.some(keyword => a.title.toLowerCase().includes(keyword)))
    .slice(0, 3)
})

const recentActivityFeed = computed(() => {
  const activities: any[] = []
  
  assessments.value.forEach(a => {
    const updated = new Date(a.updated_at)
    const created = new Date(a.created_at)
    
    // Always add a created event
    activities.push({
      id: `${a.id}-created`,
      type: 'creation',
      text: `Project Manager ${a.project_manager} created draft for "${a.title}".`,
      time: created,
      icon: 'blue'
    })
    
    // Add event based on current status
    if (['Submitted', 'Requires Full PIA', 'Under Review'].includes(a.status)) {
      activities.push({
        id: `${a.id}-submit`,
        type: 'submission',
        text: `Project Manager ${a.project_manager} submitted "${a.title}" for review.`,
        time: updated,
        icon: 'blue'
      })
    } else if (a.status === 'Returned') {
      activities.push({
        id: `${a.id}-returned`,
        type: 'returned',
        text: `DPO returned "${a.title}" for mitigation.`,
        time: updated,
        icon: 'gold'
      })
    } else if (a.status === 'Full PIA Completed') {
      activities.push({
        id: `${a.id}-completed`,
        type: 'completed',
        text: `DPO completed Full PIA for "${a.title}".`,
        time: updated,
        icon: 'green'
      })
    }
  })
  
  return activities
    .sort((a, b) => b.time.getTime() - a.time.getTime())
    .slice(0, 5)
})

const formatTimeAgo = (date: Date) => {
  const seconds = Math.floor((new Date().getTime() - date.getTime()) / 1000)
  let interval = seconds / 31536000
  if (interval > 1) return Math.floor(interval) + " years ago"
  interval = seconds / 2592000
  if (interval > 1) return Math.floor(interval) + " months ago"
  interval = seconds / 86400
  if (interval > 1) return Math.floor(interval) + " days ago"
  interval = seconds / 3600
  if (interval > 1) return Math.floor(interval) + " hours ago"
  interval = seconds / 60
  if (interval > 1) return Math.floor(interval) + " mins ago"
  return "Just now"
}

// --- Calendar Logic ---
const currentDate = ref(new Date())

const currentMonthName = computed(() => {
  return currentDate.value.toLocaleString('default', { month: 'long', year: 'numeric' }).toUpperCase()
})

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()
  
  const firstDayOfMonth = new Date(year, month, 1)
  const lastDayOfMonth = new Date(year, month + 1, 0)
  
  const startingDayOfWeek = firstDayOfMonth.getDay()
  let offset = startingDayOfWeek - 1
  if (offset === -1) offset = 6 // Sunday
  
  const days = []
  
  // Previous month padding
  const prevMonthLastDay = new Date(year, month, 0).getDate()
  for (let i = 0; i < offset; i++) {
    days.push({
      date: new Date(year, month - 1, prevMonthLastDay - offset + i + 1),
      isCurrentMonth: false
    })
  }
  
  // Current month days
  for (let i = 1; i <= lastDayOfMonth.getDate(); i++) {
    days.push({
      date: new Date(year, month, i),
      isCurrentMonth: true
    })
  }
  
  // Next month padding
  const totalDays = days.length
  const paddingNeeded = totalDays % 7 === 0 ? 0 : 7 - (totalDays % 7)
  for (let i = 1; i <= paddingNeeded; i++) {
    days.push({
      date: new Date(year, month + 1, i),
      isCurrentMonth: false
    })
  }
  
  return days
})

// Assume 14 days deadline for active tasks
const deadlines = computed(() => {
  return assessments.value
    .filter(a => ['Submitted', 'Under Review', 'Requires Full PIA'].includes(a.status))
    .map(a => {
      const created = new Date(a.created_at)
      created.setDate(created.getDate() + 14) 
      return {
        ...a,
        deadline: created
      }
    })
})

const getDeadlinesForDate = (date: Date) => {
  return deadlines.value.filter(d => 
    d.deadline.getDate() === date.getDate() &&
    d.deadline.getMonth() === date.getMonth() &&
    d.deadline.getFullYear() === date.getFullYear()
  )
}

const isToday = (date: Date) => {
  const today = new Date()
  return date.getDate() === today.getDate() && 
         date.getMonth() === today.getMonth() && 
         date.getFullYear() === today.getFullYear()
}

const prevMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1, 1)
}

const nextMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1, 1)
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
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
          <input type="text" placeholder="Search assessments..." />
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
          <button class="btn-primary" @click="router.push('/dpo/questions')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="btn-icon">
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            MANAGE QUESTIONS
          </button>
        </div>

        <!-- Premium Metrics Cards -->
        <div class="metrics-row">
          <div class="metric-card bg-glass-blue">
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
              </svg>
            </div>
          </div>

          <div class="metric-card bg-glass-red">
            <div class="metric-content">
              <span class="metric-label text-red">RISK ANALYSIS REQD</span>
              <div class="value-row">
                <span class="metric-value text-red">{{ riskAnalysisReqdCount }}</span>
                <span v-if="riskAnalysisReqdCount > 0" class="trend up text-red">↑</span>
              </div>
            </div>
            <div class="metric-icon-box bg-red">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
              </svg>
            </div>
          </div>

          <div class="metric-card bg-glass-gold">
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

          <div class="metric-card bg-glass-green">
            <div class="metric-content">
              <span class="metric-label text-green-dark">FULL PIAS COMPLETED</span>
              <span class="metric-value text-green-dark">{{ fullPiasCompletedCount }}</span>
            </div>
            <div class="metric-icon-box bg-green-dark">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
              </svg>
            </div>
          </div>

          <div class="metric-card bg-glass-purple">
            <div class="metric-content">
              <span class="metric-label text-purple-dark">AVG TURNAROUND</span>
              <div class="value-row">
                <span class="metric-value text-purple-dark">{{ averageTurnaroundTime }}</span>
                <span class="trend text-purple-dark">Days</span>
              </div>
            </div>
            <div class="metric-icon-box bg-purple-dark">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
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
              <div v-if="priorityQueue.length === 0" class="empty-state">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                <p>No pending assessments in queue.</p>
              </div>
              <div v-for="task in priorityQueue" :key="task.id" class="task-item">
                <div class="task-content">
                  <div class="task-top">
                    <div class="task-badge-row">
                      <span class="task-indicator" :class="['Submitted', 'Requires Full PIA'].includes(task.status) ? 'bg-red' : 'bg-gold-dark'"></span>
                      <span class="tag" :class="['Submitted', 'Requires Full PIA'].includes(task.status) ? 'tag-red' : 'tag-gold'">
                        {{ ['Submitted', 'Requires Full PIA'].includes(task.status) ? 'NEW SUBMISSION' : 'UNDER REVIEW' }}
                      </span>
                    </div>
                    <span class="task-due">Created: {{ new Date(task.created_at).toLocaleDateString() }}</span>
                  </div>
                  <h4 class="task-title">{{ task.title }}</h4>
                  <p class="task-meta">Initiator: <strong>{{ task.project_manager }}</strong></p>
                </div>
                <div class="task-actions">
                  <button class="btn-review" @click="router.push(`/dpo/dpia/${task.id}`)">Review</button>
                </div>
              </div>
            </div>

            <!-- High Risk Assessments -->
            <div class="section-header" style="margin-top: 40px">
              <h2 class="section-title text-red" style="display: flex; align-items: center; gap: 8px;">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 20px; height: 20px;">
                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                  <line x1="12" y1="9" x2="12" y2="13"></line>
                  <line x1="12" y1="17" x2="12.01" y2="17"></line>
                </svg>
                High-Risk Flagged Tasks
              </h2>
            </div>
            
            <div class="task-list">
              <div v-if="highRiskAssessments.length === 0" class="empty-state">
                <p>No high-risk active assessments flagged.</p>
              </div>
              <div v-for="task in highRiskAssessments" :key="task.id" class="task-item high-risk-item" style="border-color: #fecaca; background: #fff5f5;">
                <div class="task-content">
                  <div class="task-top">
                    <span class="tag tag-red">URGENT RISK</span>
                  </div>
                  <h4 class="task-title" style="color: #991b1b;">{{ task.title }}</h4>
                  <p class="task-meta">Initiator: <strong>{{ task.project_manager }}</strong></p>
                </div>
                <div class="task-actions">
                  <button class="btn-review" style="background: #dc2626; color: white;" @click="router.push(`/dpo/dpia/${task.id}`)">Prioritize Review</button>
                </div>
              </div>
            </div>

          </div>

          <!-- Side Column -->
          <div class="side-column">
            <div class="section-header">
              <h2 class="section-title">Upcoming Deadlines</h2>
            </div>
            
            <!-- Dynamic Calendar Widget -->
            <div class="calendar-widget">
              <div class="calendar-header">
                <span class="month">{{ currentMonthName }}</span>
                <div class="calendar-nav">
                  <button class="cal-btn" @click="prevMonth">&lt;</button>
                  <button class="cal-btn" @click="nextMonth">&gt;</button>
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

                <div 
                  v-for="(day, idx) in calendarDays" 
                  :key="idx"
                  :class="[
                    'day', 
                    { 
                      'muted': !day.isCurrentMonth,
                      'active-red': getDeadlinesForDate(day.date).length > 0,
                      'today': isToday(day.date)
                    }
                  ]"
                  :title="getDeadlinesForDate(day.date).map(d => d.title).join(', ')"
                >
                  {{ day.date.getDate() }}
                </div>
              </div>
            </div>

            <div class="section-header" style="margin-top: 32px">
              <h2 class="section-title">Recent Activity</h2>
            </div>
            <div class="notifications-list">
              <div v-if="recentActivityFeed.length === 0" class="empty-state">
                <p>No recent activity found.</p>
              </div>
              <div v-for="activity in recentActivityFeed" :key="activity.id" class="notification-item">
                <div class="notif-icon" :class="activity.icon">
                  <svg v-if="activity.type === 'creation'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="12" y1="18" x2="12" y2="12"></line><line x1="9" y1="15" x2="15" y2="15"></line></svg>
                  <svg v-if="activity.type === 'submission'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                  <svg v-if="activity.type === 'returned'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path><path d="M3 3v5h5"></path></svg>
                  <svg v-if="activity.type === 'completed'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                </div>
                <div class="notif-content">
                  <p>{{ activity.text }}</p>
                  <span class="notif-time">{{ formatTimeAgo(activity.time) }}</span>
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

.search-bar {
  display: flex;
  align-items: center;
  background: #f1f5f9;
  border-radius: 8px;
  padding: 0 16px;
  width: 380px;
  height: 40px;
  border: 1px solid transparent;
  transition: all 0.2s;
}

.search-bar:focus-within {
  background: #ffffff;
  border-color: #F58425;
  box-shadow: 0 0 0 3px rgba(245, 132, 37, 0.1);
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

/* Dashboard Area */
.dashboard-scroll-area {
  padding: 40px;
  overflow-y: auto;
  flex: 1;
}

.dashboard-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 32px;
}

.page-title {
  font-size: 28px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 6px;
  letter-spacing: -0.02em;
}

.page-subtitle {
  font-size: 15px;
  color: #64748b;
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

.btn-icon {
  width: 18px;
  height: 18px;
}

/* Premium Metrics Row */
.metrics-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}

.metric-card {
  border-radius: 16px;
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
}

.bg-glass-blue {
  background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
}
.bg-glass-red {
  background: linear-gradient(135deg, #ffffff 0%, #fef2f2 100%);
  border-color: #fee2e2;
}
.bg-glass-gold {
  background: linear-gradient(135deg, #ffffff 0%, #fffbeb 100%);
  border-color: #fef3c7;
}
.bg-glass-green {
  background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
  border-color: #dcfce7;
}
.bg-glass-purple {
  background: linear-gradient(135deg, #ffffff 0%, #f5f3ff 100%);
  border-color: #ede9fe;
}

.metric-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.metric-label {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: #64748b;
}

.metric-value {
  font-size: 40px;
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
  font-weight: 700;
}

.text-red {
  color: #dc2626;
}
.text-gold-dark {
  color: #b45309;
}
.text-green-dark {
  color: #15803d;
}
.text-purple-dark {
  color: #6d28d9;
}

.metric-icon-box {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.bg-blue {
  background: #0f172a;
  color: #ffffff;
}
.bg-red {
  background: #ef4444;
  color: #ffffff;
}
.bg-gold-dark {
  background: #F58425;
  color: #ffffff;
}
.bg-green-dark {
  background: #22c55e;
  color: #ffffff;
}
.bg-purple-dark {
  background: #7c3aed;
  color: #ffffff;
}

.metric-icon-box svg {
  width: 24px;
  height: 24px;
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 32px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
}

.view-all {
  font-size: 13px;
  font-weight: 600;
  color: #F58425;
  text-decoration: none;
}

/* Priority Queue */
.task-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.task-item {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
  transition: all 0.2s;
}

.task-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.06);
  border-color: #cbd5e1;
}

.task-top {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}

.task-badge-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.task-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.tag {
  font-size: 11px;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 6px;
  letter-spacing: 0.05em;
}

.tag-red {
  background: #fef2f2;
  color: #dc2626;
}
.tag-gold {
  background: #fff7ed;
  color: #ea580c;
}

.task-due {
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
}

.task-title {
  font-size: 17px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 6px;
}

.task-meta {
  font-size: 14px;
  color: #64748b;
}
.task-meta strong {
  color: #334155;
  font-weight: 600;
}

.btn-review {
  background: #f1f5f9;
  color: #0f172a;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-review:hover {
  background: #0f172a;
  color: #ffffff;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background: #f8fafc;
  border: 2px dashed #cbd5e1;
  border-radius: 16px;
  color: #64748b;
  text-align: center;
}
.empty-state svg {
  width: 48px;
  height: 48px;
  margin-bottom: 12px;
  color: #94a3b8;
}

/* Dynamic Calendar Widget */
.calendar-widget {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.02);
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.month {
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 0.05em;
  color: #0f172a;
}

.calendar-nav {
  display: flex;
  gap: 8px;
}

.cal-btn {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #475569;
  font-weight: 700;
  transition: all 0.2s;
}
.cal-btn:hover {
  background: #e2e8f0;
  color: #0f172a;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 12px 8px;
  text-align: center;
}

.day-label {
  font-size: 11px;
  font-weight: 700;
  color: #94a3b8;
  margin-bottom: 8px;
}

.day {
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  margin: 0 auto;
  cursor: default;
  transition: all 0.2s;
}

.day.muted {
  color: #cbd5e1;
}

.day.active-red {
  background: #fef2f2;
  color: #ef4444;
  border: 1px solid #fecaca;
  font-weight: 800;
  cursor: pointer;
}
.day.active-red:hover {
  background: #ef4444;
  color: #ffffff;
}

.day.today {
  background: #0f172a;
  color: #ffffff;
}
.day.today.active-red {
  background: #ef4444;
  border-color: #ef4444;
}

/* System Notifications */
.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.notification-item {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 16px;
  display: flex;
  gap: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.02);
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
.notif-icon.gold {
  color: #d97706;
}
.notif-icon.green {
  color: #22c55e;
}
.notif-icon.gray {
  color: #94a3b8;
}

.notif-content p {
  font-size: 13px;
  color: #334155;
  line-height: 1.5;
  margin: 0 0 8px 0;
}

.notif-time {
  font-size: 11px;
  font-weight: 600;
  color: #94a3b8;
}
</style>
