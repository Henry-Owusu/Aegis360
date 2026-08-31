<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AdminLayout from './components/AdminLayout.vue'
import { dpiaApi, usersApi } from '@/services/api'

const router = useRouter()

const totalAssessments = ref(0)
const totalUsers = ref(0)
const pendingReviews = ref(0)
const isLoading = ref(true)

const fetchDashboardData = async () => {
  isLoading.value = true
  try {
    const [assessmentsRes, usersRes] = await Promise.all([
      dpiaApi.listAssessments(),
      usersApi.listUsers()
    ])
    
    totalAssessments.value = assessmentsRes.total
    totalUsers.value = usersRes.total
    
    // For pending reviews, count assessments not in 'approved' or 'rejected'
    pendingReviews.value = assessmentsRes.assessments.filter(a => 
      a.status !== 'approved' && a.status !== 'rejected' && a.status !== 'draft'
    ).length
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchDashboardData)
</script>

<template>
  <AdminLayout>
    <div class="dashboard-grid">
      <!-- Total Sales (Assessments) -->
      <div class="dark-card">
        <div class="card-header">
          <div class="card-title-group">
            <div class="icon-wrap primary">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
              </svg>
            </div>
            <h3>Total Assessments</h3>
          </div>
          <button class="more-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="1"></circle>
              <circle cx="19" cy="12" r="1"></circle>
              <circle cx="5" cy="12" r="1"></circle>
            </svg>
          </button>
        </div>
        <div class="card-body">
          <div class="value">{{ isLoading ? '...' : totalAssessments }}</div>
          <div class="trend positive">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
              <polyline points="17 6 23 6 23 12"></polyline>
            </svg>
            <span>12.08% <span class="trend-sub">+120 today</span></span>
          </div>
        </div>
        <div class="card-footer">
          <button class="view-link" @click="router.push('/admin/assessments')">View Report &rarr;</button>
        </div>
      </div>

      <!-- Total Orders (Active Users) -->
      <div class="dark-card">
        <div class="card-header">
          <div class="card-title-group">
            <div class="icon-wrap secondary">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <h3>Total Users</h3>
          </div>
          <button class="more-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="1"></circle>
              <circle cx="19" cy="12" r="1"></circle>
              <circle cx="5" cy="12" r="1"></circle>
            </svg>
          </button>
        </div>
        <div class="card-body">
          <div class="value">{{ isLoading ? '...' : totalUsers }}</div>
          <div class="trend positive">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
              <polyline points="17 6 23 6 23 12"></polyline>
            </svg>
            <span>09.08% <span class="trend-sub">+1,205 today</span></span>
          </div>
        </div>
        <div class="card-footer">
          <button class="view-link" @click="router.push('/admin/users')">View Users &rarr;</button>
        </div>
      </div>

      <!-- Pending Reviews -->
      <div class="dark-card">
        <div class="card-header">
          <div class="card-title-group">
            <div class="icon-wrap warning">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
            </div>
            <h3>Pending Reviews</h3>
          </div>
          <button class="more-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="1"></circle>
              <circle cx="19" cy="12" r="1"></circle>
              <circle cx="5" cy="12" r="1"></circle>
            </svg>
          </button>
        </div>
        <div class="card-body">
          <div class="value">{{ isLoading ? '...' : pendingReviews }}</div>
          <div class="trend negative">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="23 18 13.5 8.5 8.5 13.5 1 6"></polyline>
              <polyline points="17 18 23 18 23 12"></polyline>
            </svg>
            <span>02.40% <span class="trend-sub">-15 today</span></span>
          </div>
        </div>
        <div class="card-footer">
          <button class="view-link" @click="router.push('/admin/assessments')">View Queue &rarr;</button>
        </div>
      </div>

      <!-- Statistics Chart (Placeholder) -->
      <div class="dark-card span-2 chart-card">
        <div class="card-header">
          <div class="card-title-group">
            <div class="icon-wrap chart">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
              </svg>
            </div>
            <h3>System Statistics</h3>
          </div>
          <button class="more-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="1"></circle>
              <circle cx="19" cy="12" r="1"></circle>
              <circle cx="5" cy="12" r="1"></circle>
            </svg>
          </button>
        </div>
        <div class="chart-container">
          <!-- Abstract representation of the curved graph -->
          <svg viewBox="0 0 1000 200" preserveAspectRatio="none" class="chart-svg">
            <path d="M0,150 Q100,50 200,100 T400,120 T600,60 T800,140 T1000,80" fill="none" stroke="#F58425" stroke-width="4"></path>
            <path d="M0,120 Q150,180 300,100 T500,150 T700,90 T900,160 T1000,110" fill="none" stroke="#FDBA74" stroke-width="4"></path>
            
            <!-- Grid lines -->
            <line x1="0" y1="50" x2="1000" y2="50" stroke="#2c2c35" stroke-width="1" stroke-dasharray="4,4"></line>
            <line x1="0" y1="100" x2="1000" y2="100" stroke="#2c2c35" stroke-width="1" stroke-dasharray="4,4"></line>
            <line x1="0" y1="150" x2="1000" y2="150" stroke="#2c2c35" stroke-width="1" stroke-dasharray="4,4"></line>
          </svg>
        </div>
      </div>

      <!-- Recent Assessments Table -->
      <div class="dark-card span-3">
        <div class="card-header border-bottom">
          <div class="card-title-group">
            <h3>Recent Assessments</h3>
          </div>
        </div>
        <div class="table-container">
          <table class="dark-table">
            <thead>
              <tr>
                <th>Assessment Name</th>
                <th>Owner</th>
                <th>Date</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Data Processing Agreement v2</td>
                <td><span class="muted">Tech Department</span></td>
                <td>Mar 24, 2023</td>
                <td><span class="status-pill positive">Completed</span></td>
              </tr>
              <tr>
                <td>HR Employee Database Migration</td>
                <td><span class="muted">HR Department</span></td>
                <td>Mar 23, 2023</td>
                <td><span class="status-pill warning">In Progress</span></td>
              </tr>
              <tr>
                <td>Third-party Vendor Integration</td>
                <td><span class="muted">Legal Team</span></td>
                <td>Mar 21, 2023</td>
                <td><span class="status-pill neutral">Draft</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<style scoped>
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.dark-card {
  background-color: #1C1C24;
  border-radius: 20px;
  padding: 24px;
  display: flex;
  flex-direction: column;
}

.span-2 {
  grid-column: span 2;
}

.span-3 {
  grid-column: span 3;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.card-header.border-bottom {
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.card-title-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.icon-wrap {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2C2C35;
}

.icon-wrap svg {
  width: 14px;
  height: 14px;
}

.icon-wrap.primary { color: #F58425; background-color: rgba(245, 132, 37, 0.15); }
.icon-wrap.secondary { color: #FDBA74; background-color: rgba(253, 186, 116, 0.15); }
.icon-wrap.warning { color: #F59E0B; background-color: rgba(245, 158, 11, 0.15); }
.icon-wrap.chart { color: #A78BFA; background-color: rgba(167, 139, 250, 0.15); }

h3 {
  font-size: 15px;
  font-weight: 600;
  color: #FFFFFF;
}

.more-btn {
  background: transparent;
  border: none;
  color: #92929D;
  cursor: pointer;
  padding: 4px;
}

.more-btn svg {
  width: 20px;
  height: 20px;
}

.card-body {
  margin-bottom: 24px;
}

.value {
  font-size: 36px;
  font-weight: 700;
  color: #FFFFFF;
  margin-bottom: 8px;
}

.trend {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
}

.trend svg {
  width: 16px;
  height: 16px;
}

.trend.positive { color: #22C55E; }
.trend.negative { color: #EF4444; }

.trend-sub {
  color: #92929D;
  font-weight: 500;
  margin-left: 4px;
}

.card-footer {
  margin-top: auto;
}

.view-link {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  color: #92929D;
  font-size: 13px;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.view-link:hover {
  color: #FFFFFF;
}

.chart-container {
  height: 220px;
  width: 100%;
  position: relative;
}

.chart-svg {
  width: 100%;
  height: 100%;
}

.table-container {
  width: 100%;
  overflow-x: auto;
}

.dark-table {
  width: 100%;
  border-collapse: collapse;
}

.dark-table th {
  text-align: left;
  padding: 16px 8px;
  color: #92929D;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.dark-table td {
  padding: 16px 8px;
  color: #FFFFFF;
  font-size: 14px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
}

.dark-table tr:last-child td {
  border-bottom: none;
}

.muted {
  color: #92929D;
}

.status-pill {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.status-pill.positive {
  background-color: rgba(34, 197, 94, 0.15);
  color: #4ADE80;
}

.status-pill.warning {
  background-color: rgba(245, 158, 11, 0.15);
  color: #FBBF24;
}

.status-pill.neutral {
  background-color: rgba(146, 146, 157, 0.15);
  color: #92929D;
}
</style>
