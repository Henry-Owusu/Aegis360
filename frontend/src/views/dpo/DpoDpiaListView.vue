<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import DpoSidebar from './components/DpoSidebar.vue'

const authStore = useAuthStore()

const assessments = ref([
  { id: 'PIA-2023-081', project: 'Cloud Transformation Q3', initiator: 'Sarah Jenkins (IT)', date: 'Oct 1, 2023', status: 'Under Review', risk: 'High' },
  { id: 'PIA-2023-082', project: 'Partner Portal V2', initiator: 'David Chen (Eng)', date: 'Sep 28, 2023', status: 'Needs Mitigation', risk: 'Medium' },
  { id: 'PIA-2023-083', project: 'HR Analytics Dashboard', initiator: 'Maria Garcia (HR)', date: 'Sep 25, 2023', status: 'Pending Review', risk: 'Low' },
  { id: 'PIA-2023-079', project: 'New Vendor Onboarding', initiator: 'Procurement Team', date: 'Sep 15, 2023', status: 'Approved', risk: 'Low' },
  { id: 'PIA-2023-078', project: 'Mobile App Tracking Update', initiator: 'Marketing', date: 'Sep 10, 2023', status: 'Approved', risk: 'Medium' },
])

const getStatusClass = (status: string) => {
  switch (status) {
    case 'Approved': return 'status-success'
    case 'Under Review': return 'status-primary'
    case 'Needs Mitigation': return 'status-warning'
    case 'Pending Review': return 'status-gray'
    default: return 'status-gray'
  }
}

const getRiskClass = (risk: string) => {
  switch (risk) {
    case 'High': return 'risk-high'
    case 'Medium': return 'risk-medium'
    case 'Low': return 'risk-low'
    default: return 'risk-low'
  }
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
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input type="text" placeholder="Search assessments..." />
        </div>

        <div class="nav-actions">
          <button class="icon-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="4" y1="21" x2="4" y2="14"></line>
              <line x1="4" y1="10" x2="4" y2="3"></line>
              <line x1="12" y1="21" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12" y2="3"></line>
              <line x1="20" y1="21" x2="20" y2="16"></line>
              <line x1="20" y1="12" x2="20" y2="3"></line>
              <line x1="1" y1="14" x2="7" y2="14"></line>
              <line x1="9" y1="8" x2="15" y2="8"></line>
              <line x1="17" y1="16" x2="23" y2="16"></line>
            </svg>
          </button>
          <button class="icon-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
          </button>

          <div class="user-profile">
            <div class="user-info">
              <span class="user-name">{{ authStore.user.name }}</span>
              <span class="user-role">{{ authStore.user.role }}</span>
            </div>
            <img :src="authStore.user.avatar" alt="Profile" class="avatar" />
          </div>
        </div>
      </header>

      <div class="dashboard-scroll-area">
        <div class="dashboard-header">
          <div>
            <h1 class="page-title">DPIA Module</h1>
            <p class="page-subtitle">View and manage all Data Privacy Impact Assessments.</p>
          </div>
        </div>

        <div class="table-card">
          <div class="table-toolbar">
            <div class="toolbar-left">
              <select class="filter-select">
                <option>All Statuses</option>
                <option>Pending Review</option>
                <option>Under Review</option>
                <option>Approved</option>
              </select>
            </div>
            <div class="toolbar-right">
              <span class="results-count">{{ assessments.length }} Assessments</span>
            </div>
          </div>

          <table class="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Project Name</th>
                <th>Initiator</th>
                <th>Submitted</th>
                <th>Risk Level</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="assessment in assessments" :key="assessment.id">
                <td class="col-id">{{ assessment.id }}</td>
                <td class="col-project">{{ assessment.project }}</td>
                <td class="col-initiator">{{ assessment.initiator }}</td>
                <td class="col-date">{{ assessment.date }}</td>
                <td class="col-risk">
                  <span class="risk-badge" :class="getRiskClass(assessment.risk)">
                    {{ assessment.risk }}
                  </span>
                </td>
                <td class="col-status">
                  <span class="status-badge" :class="getStatusClass(assessment.status)">
                    {{ assessment.status }}
                  </span>
                </td>
                <td class="col-action">
                  <button class="btn-sm btn-outline">View</button>
                </td>
              </tr>
            </tbody>
          </table>
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

.nav-actions {
  display: flex;
  align-items: center;
  gap: 24px;
}

.icon-btn {
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

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
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

/* Dashboard Content */
.dashboard-scroll-area {
  padding: 32px;
  overflow-y: auto;
  flex: 1;
}

.dashboard-header {
  margin-bottom: 24px;
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

.col-initiator,
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

.risk-high { background: #fee2e2; color: #b91c1c; }
.risk-medium { background: #fef3c7; color: #b45309; }
.risk-low { background: #f1f5f9; color: #475569; }

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

.status-success { color: #059669; }
.status-success::before { background: #10b981; }

.status-primary { color: #0f172a; }
.status-primary::before { background: #3b82f6; }

.status-warning { color: #b45309; }
.status-warning::before { background: #f59e0b; }

.status-gray { color: #64748b; }
.status-gray::before { background: #94a3b8; }

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
</style>
