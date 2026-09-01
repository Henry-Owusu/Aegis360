<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import DpoSidebar from './components/DpoSidebar.vue'

const authStore = useAuthStore()
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
          <input type="text" placeholder="Search reports..." />
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
            <h1 class="page-title">Compliance Reports</h1>
            <p class="page-subtitle">
              Aggregated metrics on privacy assessments and identified risks.
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
              <span class="kpi-label">DPIAs Completed (YTD)</span>
              <div class="kpi-value-row">
                <span class="kpi-value">124</span>
                <span class="trend up">↑ 12%</span>
              </div>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">Avg. Review Time</span>
              <div class="kpi-value-row">
                <span class="kpi-value">3.2</span>
                <span class="kpi-unit">days</span>
                <span class="trend down">↓ 0.5 days</span>
              </div>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">Unmitigated High Risks</span>
              <div class="kpi-value-row">
                <span class="kpi-value text-red">7</span>
                <span class="trend up text-red">↑ 2</span>
              </div>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">Compliance Score</span>
              <div class="kpi-value-row">
                <span class="kpi-value text-green">94%</span>
                <span class="trend up text-green">↑ 1%</span>
              </div>
            </div>
          </div>

          <!-- Charts Area (Mockup) -->
          <div class="charts-row">
            <div class="chart-card large">
              <div class="chart-header">
                <h3>Assessment Volume by Month</h3>
                <select class="chart-filter">
                  <option>2023</option>
                </select>
              </div>
              <div class="chart-placeholder bar-chart">
                <!-- Mock Bar Chart -->
                <div class="bar-col">
                  <div class="bar" style="height: 40%"></div>
                  <span class="x-label">Jan</span>
                </div>
                <div class="bar-col">
                  <div class="bar" style="height: 60%"></div>
                  <span class="x-label">Feb</span>
                </div>
                <div class="bar-col">
                  <div class="bar" style="height: 35%"></div>
                  <span class="x-label">Mar</span>
                </div>
                <div class="bar-col">
                  <div class="bar" style="height: 80%"></div>
                  <span class="x-label">Apr</span>
                </div>
                <div class="bar-col">
                  <div class="bar" style="height: 55%"></div>
                  <span class="x-label">May</span>
                </div>
                <div class="bar-col">
                  <div class="bar" style="height: 90%"></div>
                  <span class="x-label">Jun</span>
                </div>
                <div class="bar-col">
                  <div class="bar" style="height: 65%"></div>
                  <span class="x-label">Jul</span>
                </div>
                <div class="bar-col">
                  <div class="bar" style="height: 75%"></div>
                  <span class="x-label">Aug</span>
                </div>
                <div class="bar-col">
                  <div class="bar" style="height: 45%"></div>
                  <span class="x-label">Sep</span>
                </div>
              </div>
            </div>

            <div class="chart-card small">
              <div class="chart-header">
                <h3>Risk Distribution</h3>
              </div>
              <div class="chart-placeholder donut-chart">
                <!-- Mock Donut Chart -->
                <div class="donut">
                  <div class="donut-inner">
                    <span class="donut-total">342</span>
                    <span class="donut-label">Total Risks</span>
                  </div>
                </div>
                <div class="chart-legend">
                  <div class="legend-item"><span class="dot red"></span> High (12%)</div>
                  <div class="legend-item"><span class="dot gold"></span> Medium (38%)</div>
                  <div class="legend-item"><span class="dot gray"></span> Low (50%)</div>
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
  margin-bottom: 32px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
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

.btn-outline {
  display: flex;
  align-items: center;
  gap: 8px;
  background: transparent;
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
}

.kpi-value {
  font-size: 32px;
  font-weight: 800;
  color: #0f172a;
  line-height: 1;
}

.kpi-unit {
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
}

.trend {
  font-size: 13px;
  font-weight: 600;
}

.trend.up {
  color: #059669;
}
.trend.down {
  color: #0ea5e9;
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

.chart-filter {
  padding: 6px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 13px;
  color: #475569;
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
  background: #0ea5e9;
  border-radius: 4px 4px 0 0;
  transition: background 0.2s;
}

.bar:hover {
  background: #0284c7;
}

.x-label {
  font-size: 12px;
  color: #64748b;
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
  background: conic-gradient(#b91c1c 0% 12%, #d97706 12% 50%, #e2e8f0 50% 100%);
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
