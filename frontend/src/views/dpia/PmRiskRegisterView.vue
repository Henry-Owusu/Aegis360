<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import PmSidebar from './components/PmSidebar.vue'

const router = useRouter()
const authStore = useAuthStore()

const risks = ref([
  { id: 'RSK-101', project: 'Cloud Transformation Q3', description: 'Data breach during migration phase', impact: 'Critical', likelihood: 'Medium', mitigation: 'End-to-end encryption, phased migration, audit logs.', status: 'Open' },
  { id: 'RSK-102', project: 'Cloud Transformation Q3', description: 'Unauthorized access via third-party API', impact: 'High', likelihood: 'High', mitigation: 'Implement OAuth 2.0, strict API rate limiting, IP whitelisting.', status: 'Mitigating' },
  { id: 'RSK-104', project: 'Mobile App Tracking Update', description: 'Non-compliance with GDPR consent requirements', impact: 'Critical', likelihood: 'Low', mitigation: 'Implement explicit opt-in banner, document consent logs.', status: 'Closed' },
])

const getStatusClass = (status: string) => {
  switch (status) {
    case 'Closed': return 'status-success'
    case 'Open': return 'status-warning'
    case 'Mitigating': return 'status-primary'
    default: return 'status-gray'
  }
}

const getSeverityClass = (severity: string) => {
  switch (severity) {
    case 'Critical': return 'risk-critical'
    case 'High': return 'risk-high'
    case 'Medium': return 'risk-medium'
    case 'Low': return 'risk-low'
    default: return 'risk-low'
  }
}

const handleNavigateModules = () => {
  router.push('/modules')
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
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
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input type="text" placeholder="Search my project risks..." class="search-input" />
        </div>
      </div>

      <!-- Right Action & Profile Section -->
      <div class="navbar-actions">
        <button type="button" class="notification-btn" title="Notifications">
          <svg class="bell-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
          </svg>
          <span class="notification-dot"></span>
        </button>

        <div class="user-profile-menu" @click="handleLogout" title="Click to Sign Out">
          <div class="user-info">
            <span class="user-name">{{ authStore.user.name }}</span>
            <span class="user-role">{{ authStore.user.role }}</span>
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
            <h1 class="page-title">Project Risk Register</h1>
            <p class="page-subtitle">Track and monitor identified privacy risks for your assigned projects.</p>
          </div>
          <button class="btn-primary">
            Export Report
          </button>
        </div>

        <div class="table-card">
          <div class="table-toolbar">
            <div class="toolbar-left">
              <select class="filter-select">
                <option>All My Projects</option>
                <option>Cloud Transformation Q3</option>
                <option>Mobile App Tracking Update</option>
              </select>
              <select class="filter-select">
                <option>All Statuses</option>
                <option>Open</option>
                <option>Mitigating</option>
                <option>Closed</option>
              </select>
            </div>
            <div class="toolbar-right">
              <span class="results-count">{{ risks.length }} Identified Risks</span>
            </div>
          </div>

          <table class="data-table">
            <thead>
              <tr>
                <th>Risk ID</th>
                <th>Project</th>
                <th>Description</th>
                <th>Impact</th>
                <th>Likelihood</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="risk in risks" :key="risk.id">
                <td class="col-id">{{ risk.id }}</td>
                <td class="col-project">{{ risk.project }}</td>
                <td class="col-desc">
                  <span class="desc-text">{{ risk.description }}</span>
                  <div class="mitigation-plan">
                    <strong>Mitigation:</strong> {{ risk.mitigation }}
                  </div>
                </td>
                <td class="col-severity">
                  <span class="severity-badge" :class="getSeverityClass(risk.impact)">
                    {{ risk.impact }}
                  </span>
                </td>
                <td class="col-severity">
                  <span class="severity-badge" :class="getSeverityClass(risk.likelihood)">
                    {{ risk.likelihood }}
                  </span>
                </td>
                <td class="col-status">
                  <span class="status-badge" :class="getStatusClass(risk.status)">
                    {{ risk.status }}
                  </span>
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
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f8fafc;
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

.btn-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #0f2942;
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
  background: #0a1f33;
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

.toolbar-left {
  display: flex;
  gap: 12px;
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
  vertical-align: top;
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
  white-space: nowrap;
}

.col-project {
  font-size: 14px;
  font-weight: 600;
  color: #0f172a;
}

.col-desc {
  max-width: 400px;
}

.desc-text {
  font-size: 14px;
  color: #0f172a;
  display: block;
  margin-bottom: 8px;
}

.mitigation-plan {
  font-size: 12px;
  color: #64748b;
  background: #f1f5f9;
  padding: 8px 12px;
  border-radius: 6px;
  line-height: 1.5;
}

.severity-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 12px;
  text-transform: uppercase;
  display: inline-block;
}

.risk-critical { background: #7f1d1d; color: #ffffff; }
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

</style>
