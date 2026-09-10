<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import PmSidebar from './components/PmSidebar.vue'
import { dpiaApi, type AssessmentSummary } from '@/services/api'

const router = useRouter()
const authStore = useAuthStore()

const assessments = ref<AssessmentSummary[]>([])
const isLoading = ref(true)

const filterStatus = ref('All Statuses')

const filteredAssessments = computed(() => {
  return assessments.value.filter((a) => {
    if (filterStatus.value === 'All Statuses') return true
    
    // Convert status to friendly label for matching the dropdown
    const friendlyStatus = getStatusLabel(a.status)
    return friendlyStatus === filterStatus.value
  })
})

const fetchData = async () => {
  isLoading.value = true
  try {
    const res = await dpiaApi.listAssessments()
    // For PMs, we ideally only want to show their own assessments.
    // Assuming backend returns all for now, we'll filter them locally if needed,
    // or assume the backend handles PM filtering.
    assessments.value = res.assessments.filter((a) => a.created_by === authStore.user.id || authStore.user.roles.includes('System Administrator'))
  } catch (err) {
    console.error('Failed to load assessments:', err)
  } finally {
    isLoading.value = false
  }
}

const formatDate = (iso: string) =>
  new Date(iso).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })

const getStatusClass = (status: string) => {
  switch (status.toLowerCase()) {
    case 'approved':
      return 'status-success'
    case 'dpo_review':
    case 'screening':
      return 'status-primary'
    case 'rejected':
      return 'status-warning'
    case 'draft':
      return 'status-gray'
    default:
      return 'status-gray'
  }
}

const getStatusLabel = (status: string) => {
  return status.charAt(0).toUpperCase() + status.slice(1).replace('_', ' ')
}

const handleNavigateModules = () => {
  router.push('/modules')
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const handleCreateAssessment = () => {
  router.push('/pm/dpia/new')
}

const submitAssessment = async (id: string) => {
  if (!confirm('Are you sure you want to submit this assessment for DPO review?')) return
  try {
    await dpiaApi.submitAssessment(id)
    fetchData() // Refresh list
  } catch (err) {
    alert('Failed to submit assessment')
  }
}

onMounted(fetchData)
</script>

<template>
  <div class="dpia-layout">
    <!-- Top Header Navigation Bar -->
    <header class="top-navbar">
      <!-- Left Logo Section -->
      <div class="navbar-brand" @click="handleNavigateModules" title="Back to Modules">
        <img src="/Aegislogo.jpeg" alt="Aegis360 Logo" class="brand-logo-img" />
      </div>

      <!-- Center Search Bar -->
      <div class="search-container">
        <div class="search-input-wrapper">
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
          <input type="text" placeholder="Search my assessments..." class="search-input" />
        </div>
      </div>

      <!-- Right Action & Profile Section -->
      <div class="navbar-actions">
        <button type="button" class="notification-btn" title="Notifications">
          <svg
            class="bell-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
          </svg>
          <span class="notification-dot"></span>
        </button>

        <div class="user-profile-menu" @click="handleLogout" title="Click to Sign Out">
          <div class="user-info">
            <span class="user-name">{{ authStore.user.name }}</span>
            <span class="user-role">{{ authStore.user.roles[0] }}</span>
          </div>
          <div class="avatar-container">
            <img :src="authStore.user.avatar" :alt="authStore.user.name" class="user-avatar" />
          </div>
        </div>
      </div>
    </header>

    <!-- Main Container -->
    <div class="body-container">
      <PmSidebar />

      <!-- Main Workspace Area -->
      <main class="main-content">
        <div class="dashboard-header">
          <div>
            <h1 class="page-title">My Assessments</h1>
            <p class="page-subtitle">Manage and track the DPIAs for your assigned projects.</p>
          </div>
          <button class="add-assessment-btn" @click="handleCreateAssessment">
            <svg
              class="plus-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.5"
            >
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            <span>New Assessment</span>
          </button>
        </div>

        <div class="table-card">
          <div class="table-toolbar">
            <div class="toolbar-left">
              <select class="filter-select" v-model="filterStatus">
                <option>All Statuses</option>
                <option>Draft</option>
                <option>Screening</option>
                <option>Dpo review</option>
                <option>Approved</option>
                <option>Rejected</option>
              </select>
            </div>
            <div class="toolbar-right">
              <span class="results-count">{{ filteredAssessments.length }} Assessments</span>
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="isLoading" style="padding: 40px; text-align: center; color: #64748b;">
            Loading assessments...
          </div>
          
          <table v-else class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Project Name</th>
                <th>Last Updated</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredAssessments.length === 0">
                <td colspan="5" style="text-align: center; padding: 32px; color: #94a3b8;">
                  No assessments found.
                </td>
              </tr>
              <tr v-for="assessment in filteredAssessments" :key="assessment.id">
                <td class="col-id">{{ assessment.id.substring(0, 8) }}</td>
                <td class="col-project">{{ assessment.title }}</td>
                <td class="col-date">{{ formatDate(assessment.updated_at) }}</td>
                <td class="col-status">
                  <span class="status-badge" :class="getStatusClass(assessment.status)">
                    {{ getStatusLabel(assessment.status) }}
                  </span>
                </td>
                <td class="col-action">
                  <button class="btn-sm btn-outline" @click="router.push(`/pm/dpia/${assessment.id}`)">Open</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
.dpia-layout {
  height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f8fafc;
  overflow: hidden;
}

/* Top Navbar */
.top-navbar {
  height: 105px;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-brand {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.brand-logo-img {
  height: 90px;
  width: auto;
  object-fit: contain;
}

.search-container {
  flex: 1;
  max-width: 480px;
  margin: 0 40px;
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 16px;
  width: 18px;
  height: 18px;
  color: #94a3b8;
}

.search-input {
  width: 100%;
  height: 44px;
  padding: 0 18px 0 46px;
  background-color: #f1f5f9;
  border: 1px solid transparent;
  border-radius: 10px;
  font-family: var(--font-family);
  font-size: 14px;
  color: #0f172a;
  outline: none;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 24px;
}

.notification-btn {
  position: relative;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  cursor: pointer;
  width: 42px;
  height: 42px;
  color: #475569;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bell-icon {
  width: 20px;
  height: 20px;
}

.notification-dot {
  position: absolute;
  top: 9px;
  right: 9px;
  width: 8px;
  height: 8px;
  background-color: #ef4444;
  border: 2px solid #ffffff;
  border-radius: 50%;
}

.user-profile-menu {
  display: flex;
  align-items: center;
  gap: 14px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 12px;
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
  font-size: 11.5px;
  color: #64748b;
  margin-top: 2px;
}

.avatar-container {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #e2e8f0;
}

.user-avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Body Container */
.body-container {
  flex: 1;
  display: flex;
  min-height: 0;
  overflow: hidden;
}

/* Main Content Workspace */
.main-content {
  flex: 1;
  padding: 36px 40px;
  background-color: #f8fafc;
  overflow-y: auto;
}

.dashboard-header {
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.page-title {
  font-family: var(--font-family);
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.02em;
  margin-bottom: 6px;
}

.page-subtitle {
  font-size: 15px;
  color: #64748b;
}

.add-assessment-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 44px;
  padding: 0 20px;
  background-color: #030712;
  color: #ffffff;
  border: none;
  border-radius: 10px;
  font-family: var(--font-family);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(3, 7, 18, 0.15);
  transition: all 0.2s;
}

.add-assessment-btn:hover {
  background-color: #111827;
  transform: translateY(-2px);
}

.plus-icon {
  width: 16px;
  height: 16px;
}

/* Table Card */
.table-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.table-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 13px;
  color: #0f172a;
  outline: none;
}

.results-count {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 16px 24px;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.data-table th {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: #ffffff;
}

.data-table tbody tr:hover {
  background: #f8fafc;
}

.col-id {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
}

.col-project {
  font-size: 14px;
  font-weight: 600;
  color: #0f172a;
}

.col-date {
  font-size: 14px;
  color: #475569;
}

.risk-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 12px;
  text-transform: uppercase;
  display: inline-block;
}

.risk-high {
  background: #fee2e2;
  color: #b91c1c;
}
.risk-medium {
  background: #fef3c7;
  color: #b45309;
}
.risk-low {
  background: #f1f5f9;
  color: #475569;
}

.status-badge {
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-badge::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-success {
  color: #059669;
}
.status-success::before {
  background: #10b981;
}

.status-primary {
  color: #0f172a;
}
.status-primary::before {
  background: #3b82f6;
}

.status-warning {
  color: #b45309;
}
.status-warning::before {
  background: #f59e0b;
}

.status-gray {
  color: #64748b;
}
.status-gray::before {
  background: #94a3b8;
}

.btn-sm {
  padding: 6px 16px;
  font-size: 13px;
  font-weight: 600;
  border-radius: 6px;
  cursor: pointer;
}

.btn-outline {
  background: transparent;
  border: 1px solid #cbd5e1;
  color: #475569;
}

.btn-outline:hover {
  background: #f1f5f9;
  color: #0f172a;
}
.action-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: 1px solid transparent;
  background-color: transparent;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.action-btn:hover {
  background-color: #f1f5f9;
  color: #0f172a;
  border-color: #cbd5e1;
}

.action-btn.submit-btn:hover {
  background-color: #eff6ff;
  color: #2563eb;
  border-color: #bfdbfe;
}

.action-btn.delete-btn:hover {
  background-color: #fef2f2;
  color: #dc2626;
  border-color: #fecaca;
}

.action-btn.download-btn:hover {
  background-color: #f0fdf4;
  color: #16a34a;
  border-color: #bbf7d0;
}
</style>
