<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import PmSidebar from './components/PmSidebar.vue'

const router = useRouter()
const authStore = useAuthStore()

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
          <input type="text" placeholder="Search reports..." class="search-input" />
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
            <h1 class="page-title">Project Portfolio Reports</h1>
            <p class="page-subtitle">
              Metrics and insights on privacy compliance across your projects.
            </p>
          </div>
          <button class="btn-outline">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              class="btn-icon"
            >
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="7 10 12 15 17 10"></polyline>
              <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
            Download PDF
          </button>
        </div>

        <div class="reports-grid">
          <!-- KPI Row -->
          <div class="kpi-row">
            <div class="kpi-card">
              <span class="kpi-label">Active DPIAs</span>
              <div class="kpi-value-row">
                <span class="kpi-value">12</span>
              </div>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">Pending DPO Approval</span>
              <div class="kpi-value-row">
                <span class="kpi-value">5</span>
                <span class="trend down">Wait time: 2 days</span>
              </div>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">Unmitigated Risks</span>
              <div class="kpi-value-row">
                <span class="kpi-value text-red">3</span>
                <span class="trend up text-red">Critical & High</span>
              </div>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">Project Compliance Score</span>
              <div class="kpi-value-row">
                <span class="kpi-value text-green">94%</span>
                <span class="trend up text-green">Target: 90%</span>
              </div>
            </div>
          </div>

          <!-- Charts Area (Mockup) -->
          <div class="charts-row">
            <div class="chart-card large">
              <div class="chart-header">
                <h3>Assessment Status by Project</h3>
              </div>
              <div class="chart-placeholder bar-chart">
                <!-- Mock Bar Chart -->
                <div class="bar-col">
                  <div class="bar approved" style="height: 100%"></div>
                  <span class="x-label">HRIS Migr</span>
                </div>
                <div class="bar-col">
                  <div class="bar review" style="height: 60%"></div>
                  <span class="x-label">Cloud Q3</span>
                </div>
                <div class="bar-col">
                  <div class="bar review" style="height: 35%"></div>
                  <span class="x-label">Partner API</span>
                </div>
                <div class="bar-col">
                  <div class="bar draft" style="height: 20%"></div>
                  <span class="x-label">Mobile Track</span>
                </div>
                <div class="bar-col">
                  <div class="bar approved" style="height: 90%"></div>
                  <span class="x-label">Vendor Onb</span>
                </div>
              </div>
            </div>

            <div class="chart-card small">
              <div class="chart-header">
                <h3>My Portfolio Risk Distribution</h3>
              </div>
              <div class="chart-placeholder donut-chart">
                <!-- Mock Donut Chart -->
                <div class="donut">
                  <div class="donut-inner">
                    <span class="donut-total">18</span>
                    <span class="donut-label">Total Risks</span>
                  </div>
                </div>
                <div class="chart-legend">
                  <div class="legend-item"><span class="dot red"></span> High (16%)</div>
                  <div class="legend-item"><span class="dot gold"></span> Medium (34%)</div>
                  <div class="legend-item"><span class="dot gray"></span> Low (50%)</div>
                </div>
              </div>
            </div>
          </div>
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
  margin-bottom: 32px;
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

.btn-outline {
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
}

.btn-outline:hover {
  background: #f1f5f9;
}

.btn-icon {
  width: 16px;
  height: 16px;
}

/* KPI Row */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.kpi-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.kpi-label {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  display: block;
  margin-bottom: 12px;
}

.kpi-value-row {
  display: flex;
  align-items: baseline;
  gap: 8px;
  flex-wrap: wrap;
}

.kpi-value {
  font-family: var(--font-family);
  font-size: 32px;
  font-weight: 800;
  color: #0f172a;
  line-height: 1;
}

.trend {
  font-size: 13px;
  font-weight: 600;
}

.trend.down {
  color: #64748b;
}
.text-red {
  color: #b91c1c !important;
}
.text-green {
  color: #059669 !important;
}

/* Charts Area */
.charts-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.chart-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.chart-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #0f172a;
}

.chart-placeholder {
  height: 300px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}

/* Mock Bar Chart CSS */
.bar-chart {
  gap: 16px;
  padding-bottom: 24px;
}

.bar-col {
  flex: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  gap: 8px;
}

.bar {
  width: 100%;
  max-width: 40px;
  border-radius: 4px 4px 0 0;
  transition: opacity 0.2s;
}

.bar:hover {
  opacity: 0.8;
}

.bar.approved {
  background: #059669;
}
.bar.review {
  background: #0ea5e9;
}
.bar.draft {
  background: #94a3b8;
}

.x-label {
  font-size: 12px;
  color: #64748b;
  white-space: nowrap;
}

/* Mock Donut Chart CSS */
.donut-chart {
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 32px;
}

.donut {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: conic-gradient(#b91c1c 0% 16%, #d97706 16% 50%, #e2e8f0 50% 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.donut-inner {
  width: 140px;
  height: 140px;
  background: #ffffff;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.donut-total {
  font-family: var(--font-family);
  font-size: 28px;
  font-weight: 800;
  color: #0f172a;
}

.donut-label {
  font-size: 12px;
  color: #64748b;
}

.chart-legend {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  padding: 0 24px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #475569;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}
.dot.red {
  background: #b91c1c;
}
.dot.gold {
  background: #d97706;
}
.dot.gray {
  background: #e2e8f0;
}
</style>
