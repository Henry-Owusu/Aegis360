<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import PmSidebar from './components/PmSidebar.vue'

const router = useRouter()
const authStore = useAuthStore()
const searchQuery = ref('')

const handleNavigateModules = () => {
  router.push('/modules')
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

const handleStartPhoenix = () => {
  router.push('/pm/dpia/new')
}

const handleViewOrion = () => {
  window.alert('Opening DPO Comments for Project Orion...')
}

const handleCreateAssessment = () => {
  router.push('/pm/dpia/new')
}
</script>

<template>
  <div class="dpia-layout">
    <!-- Top Header Navigation Bar -->
    <header class="top-navbar">
      <!-- Left Logo Section (Navigates back to Modules on click) -->
      <div class="navbar-brand" @click="handleNavigateModules" title="Back to Modules">
        <img src="/Aegislogo.jpeg" alt="Aegis360 Logo" class="brand-logo-img" />
      </div>

      <!-- Center Search Bar -->
      <div class="search-container">
        <div class="search-input-wrapper">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search ERP data..."
            class="search-input"
          />
        </div>
      </div>

      <!-- Right Action & Profile Section -->
      <div class="navbar-actions">
        <!-- Notification Bell -->
        <button type="button" class="notification-btn" title="Notifications">
          <svg class="bell-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
          </svg>
          <span class="notification-dot"></span>
        </button>

        <!-- User Profile Dropdown -->
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

    <!-- Main Container with Left Sidebar & PM Dashboard Content -->
    <div class="body-container">
      <!-- Left Sidebar Navigation -->
      <PmSidebar />

      <!-- Main Workspace Area -->
      <main class="main-content">
        <!-- PM Dashboard Hero Section -->
        <header class="pm-hero">
          <div class="pm-hero-left">
            <span class="pm-tag">PROJECT MANAGER DASHBOARD</span>
            <h1 class="pm-title">System Status Optimal</h1>
            <p class="pm-desc">
              You have pending tasks requiring attention. Your current privacy assessment pipeline indicates a bottleneck in DPO reviews.
            </p>
          </div>
          <div class="pm-hero-right">
            <button type="button" class="add-assessment-btn" @click="handleCreateAssessment">
              <svg class="plus-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
              <span>Add Assessment</span>
            </button>
          </div>
        </header>

        <!-- Dashboard Grid (2 Columns: Main Content Left + Widgets Right) -->
        <div class="dashboard-grid">
          <!-- Left Column -->
          <div class="grid-left-col">
            <!-- Top Metric Cards Grid (3 Cards) -->
            <div class="metric-cards-row">
              <!-- Metric Card 1: DRAFT DPIAS -->
              <div class="metric-card">
                <div class="metric-header">
                  <span class="metric-label">DRAFT DPIAS</span>
                  <div class="metric-icon-box">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                      <polyline points="14 2 14 8 20 8"></polyline>
                    </svg>
                  </div>
                </div>
                <div class="metric-body">
                  <span class="metric-number">12</span>
                  <span class="metric-trend">↑ +3</span>
                </div>
              </div>

              <!-- Metric Card 2: AWAITING DPO REVIEW -->
              <div class="metric-card">
                <div class="metric-header">
                  <span class="metric-label">AWAITING DPO REVIEW</span>
                  <div class="metric-icon-box">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"></circle>
                      <polyline points="12 6 12 12 16 14"></polyline>
                    </svg>
                  </div>
                </div>
                <div class="metric-body">
                  <span class="metric-number">5</span>
                  <span class="attention-tag">Needs attention</span>
                </div>
              </div>

              <!-- Metric Card 3: RETURNED FOR FEEDBACK -->
              <div class="metric-card">
                <div class="metric-header">
                  <span class="metric-label">RETURNED FOR FEEDBACK</span>
                  <div class="metric-icon-box alert-box">
                    <svg viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2">
                      <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                      <line x1="12" y1="9" x2="12" y2="13"></line>
                      <line x1="12" y1="17" x2="12.01" y2="17"></line>
                    </svg>
                  </div>
                </div>
                <div class="metric-body">
                  <span class="metric-number">2</span>
                  <span class="metric-dots">•••</span>
                </div>
              </div>
            </div>

            <!-- Tasks Inbox Container -->
            <div class="panel-box tasks-inbox-panel">
              <div class="panel-header">
                <h2 class="panel-title">Tasks Inbox</h2>
                <span class="action-required-badge">ACTION REQUIRED</span>
              </div>

              <div class="tasks-list">
                <!-- Task 1: Complete screening for Project Phoenix -->
                <div class="task-row">
                  <div class="task-left">
                    <div class="task-thumb-box">
                      <img src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=100&auto=format&fit=crop&q=80" alt="Building thumbnail" class="task-thumb-img" />
                      <span class="alert-icon-badge">!</span>
                    </div>
                    <div class="task-info">
                      <h3 class="task-name">Complete screening for Project Phoenix</h3>
                      <div class="task-tags">
                        <span class="tag-critical">Critical</span>
                        <span class="tag-meta">• Due Today</span>
                      </div>
                    </div>
                  </div>
                  <button type="button" class="task-btn primary-task-btn" @click="handleStartPhoenix">
                    Start
                  </button>
                </div>

                <!-- Task 2: Respond to DPO comments -->
                <div class="task-row">
                  <div class="task-left">
                    <div class="task-icon-box comment-box">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                      </svg>
                    </div>
                    <div class="task-info">
                      <h3 class="task-name">Respond to DPO comments</h3>
                      <div class="task-tags">
                        <span class="tag-review">Review</span>
                        <span class="tag-meta">• Project Orion DPIA</span>
                      </div>
                    </div>
                  </div>
                  <button type="button" class="task-btn secondary-task-btn" @click="handleViewOrion">
                    View
                  </button>
                </div>
              </div>
            </div>

            <!-- Recently Completed Container -->
            <div class="panel-box recently-completed-panel">
              <div class="panel-header">
                <h2 class="panel-title">Recently Completed</h2>
                <a href="#view-all" class="view-all-link" @click.prevent>View All</a>
              </div>

              <div class="completed-list">
                <div class="completed-item">
                  <div class="item-left">
                    <div class="check-circle-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <polyline points="20 6 9 17 4 12"></polyline>
                      </svg>
                    </div>
                    <span class="completed-text">Vendor Assessment: CloudTech Inc.</span>
                  </div>
                  <span class="time-ago">2 HRS AGO</span>
                </div>

                <div class="completed-item">
                  <div class="item-left">
                    <div class="check-circle-icon">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                        <polyline points="20 6 9 17 4 12"></polyline>
                      </svg>
                    </div>
                    <span class="completed-text">Data Flow Mapping: HR Portal</span>
                  </div>
                  <span class="time-ago">YESTERDAY</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column Widgets -->
          <div class="grid-right-col">
            <!-- Global Compliance Score Card -->
            <div class="panel-box compliance-score-panel">
              <h3 class="widget-title">GLOBAL COMPLIANCE SCORE</h3>

              <!-- SVG Circular Donut Chart -->
              <div class="donut-chart-container">
                <svg class="donut-svg" viewBox="0 0 100 100">
                  <!-- Background Track Ring -->
                  <circle
                    cx="50"
                    cy="50"
                    r="40"
                    fill="none"
                    stroke="#e0f2fe"
                    stroke-width="9"
                  />
                  <!-- Progress Segment Ring (94% = 236 out of 251 circumference) -->
                  <circle
                    cx="50"
                    cy="50"
                    r="40"
                    fill="none"
                    stroke="#008080"
                    stroke-width="9"
                    stroke-dasharray="251.2"
                    stroke-dashoffset="15"
                    stroke-linecap="round"
                    transform="rotate(-90 50 50)"
                  />
                </svg>
                <div class="donut-center-text">
                  <span class="score-number">94%</span>
                </div>
              </div>

              <p class="compliance-caption">
                Your organization is operating within acceptable risk parameters.
              </p>
            </div>

            <!-- Activity Feed Widget -->
            <div class="panel-box activity-feed-panel">
              <h3 class="widget-title">Activity Feed</h3>

              <div class="activity-timeline">
                <!-- Activity Item 1 -->
                <div class="timeline-item">
                  <div class="timeline-dot"></div>
                  <div class="timeline-content">
                    <span class="timeline-time">JUST NOW</span>
                    <p class="timeline-desc">
                      You assigned <strong>Project Phoenix</strong> to the screening queue.
                    </p>
                  </div>
                </div>

                <!-- Activity Item 2 -->
                <div class="timeline-item">
                  <div class="timeline-dot teal"></div>
                  <div class="timeline-content">
                    <span class="timeline-time">2 HOURS AGO</span>
                    <p class="timeline-desc">
                      <strong>DPO Marcus Vance</strong> reviewed Project Orion.
                    </p>
                    <div class="quote-box">
                      "Please clarify section 4 regarding data retention periods before final approval."
                    </div>
                  </div>
                </div>

                <!-- Activity Item 3 -->
                <div class="timeline-item">
                  <div class="timeline-dot gray"></div>
                  <div class="timeline-content">
                    <span class="timeline-time">YESTERDAY</span>
                    <p class="timeline-desc">
                      System generated weekly compliance digest.
                    </p>
                  </div>
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

/* PM Hero Banner */
.pm-hero {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 28px;
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
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.add-assessment-btn:hover {
  background-color: #111827;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(3, 7, 18, 0.25);
}

.add-assessment-btn:active {
  transform: translateY(0);
}

.plus-icon {
  width: 16px;
  height: 16px;
}

.pm-tag {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #0d9488;
  display: inline-block;
  margin-bottom: 6px;
}

.pm-title {
  font-family: var(--font-family);
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.02em;
}

.pm-desc {
  font-size: 14px;
  color: #64748b;
  margin-top: 6px;
  max-width: 620px;
  line-height: 1.5;
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 24px;
}

/* Left Column Layout */
.grid-left-col {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Metric Cards Row */
.metric-cards-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.metric-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 120px;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
}

.metric-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}

.metric-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #64748b;
  text-transform: uppercase;
  max-width: 140px;
  line-height: 1.3;
}

.metric-icon-box {
  width: 32px;
  height: 32px;
  background: #f8fafc;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
}

.metric-icon-box svg {
  width: 16px;
  height: 16px;
}

.metric-icon-box.alert-box {
  background: #fef2f2;
}

.metric-body {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-top: 16px;
}

.metric-number {
  font-family: var(--font-family);
  font-size: 32px;
  font-weight: 700;
  color: #0f172a;
  line-height: 1;
}

.metric-trend {
  font-size: 13px;
  font-weight: 600;
  color: #0d9488;
}

.attention-tag {
  font-size: 11px;
  font-weight: 600;
  color: #b45309;
  background: #fffbeb;
  padding: 3px 8px;
  border-radius: 6px;
}

.metric-dots {
  color: #ef4444;
  font-weight: 900;
  letter-spacing: 2px;
}

/* Panel Box Containers */
.panel-box {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.panel-title {
  font-family: var(--font-family);
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
}

.action-required-badge {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #0284c7;
  background: #e0f2fe;
  padding: 4px 10px;
  border-radius: 6px;
}

/* Tasks Inbox */
.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.task-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  background: #f8fafc;
  border: 1px solid #f1f5f9;
  border-radius: 12px;
}

.task-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.task-thumb-box {
  position: relative;
  width: 44px;
  height: 44px;
  border-radius: 8px;
  overflow: hidden;
}

.task-thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.alert-icon-badge {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 14px;
  height: 14px;
  background: #ef4444;
  color: #ffffff;
  border-radius: 50%;
  font-size: 10px;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
}

.task-icon-box {
  width: 44px;
  height: 44px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.task-icon-box.comment-box {
  background: #fef3c7;
  color: #b45309;
}

.task-icon-box svg {
  width: 20px;
  height: 20px;
}

.task-name {
  font-size: 14.5px;
  font-weight: 600;
  color: #0f172a;
}

.task-tags {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 4px;
}

.tag-critical {
  font-size: 11px;
  font-weight: 600;
  color: #ef4444;
  background: #fef2f2;
  padding: 2px 6px;
  border-radius: 4px;
}

.tag-review {
  font-size: 11px;
  font-weight: 600;
  color: #b45309;
  background: #fef3c7;
  padding: 2px 6px;
  border-radius: 4px;
}

.tag-meta {
  font-size: 12px;
  color: #64748b;
}

.task-btn {
  height: 36px;
  padding: 0 20px;
  border-radius: 8px;
  font-family: var(--font-family);
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.15s ease;
}

.primary-task-btn {
  background-color: #030712;
  color: #ffffff;
}

.primary-task-btn:hover {
  background-color: #111827;
}

.secondary-task-btn {
  background-color: #f1f5f9;
  color: #334155;
  border: 1px solid #e2e8f0;
}

.secondary-task-btn:hover {
  background-color: #e2e8f0;
}

/* Recently Completed */
.view-all-link {
  font-size: 13px;
  font-weight: 600;
  color: #0d9488;
  text-decoration: none;
}

.completed-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.completed-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  background: #f8fafc;
  border-radius: 10px;
}

.item-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.check-circle-icon {
  width: 22px;
  height: 22px;
  background: #ccfbf1;
  color: #0d9488;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.check-circle-icon svg {
  width: 13px;
  height: 13px;
}

.completed-text {
  font-size: 13.5px;
  font-weight: 500;
  color: #334155;
}

.time-ago {
  font-size: 11px;
  font-weight: 600;
  color: #94a3b8;
  letter-spacing: 0.05em;
}

/* Right Column Widgets */
.grid-right-col {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.widget-title {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #64748b;
  text-transform: uppercase;
  margin-bottom: 18px;
}

/* Compliance Score Widget */
.compliance-score-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.donut-chart-container {
  position: relative;
  width: 140px;
  height: 140px;
  margin: 12px 0;
}

.donut-svg {
  width: 100%;
  height: 100%;
}

.donut-center-text {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.score-number {
  font-family: var(--font-family);
  font-size: 26px;
  font-weight: 800;
  color: #0f172a;
}

.compliance-caption {
  font-size: 12.5px;
  color: #64748b;
  line-height: 1.4;
  margin-top: 8px;
  max-width: 240px;
}

/* Activity Feed */
.activity-timeline {
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: relative;
  padding-left: 12px;
}

.activity-timeline::before {
  content: '';
  position: absolute;
  top: 6px;
  bottom: 6px;
  left: 15px;
  width: 2px;
  background: #e2e8f0;
}

.timeline-item {
  position: relative;
  padding-left: 20px;
}

.timeline-dot {
  position: absolute;
  left: 0;
  top: 4px;
  width: 8px;
  height: 8px;
  background: #0f172a;
  border-radius: 50%;
  z-index: 2;
  box-shadow: 0 0 0 3px #ffffff;
}

.timeline-dot.teal {
  background: #0d9488;
}

.timeline-dot.gray {
  background: #cbd5e1;
}

.timeline-time {
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #94a3b8;
  display: block;
  margin-bottom: 2px;
}

.timeline-desc {
  font-size: 13px;
  color: #334155;
  line-height: 1.4;
}

.quote-box {
  margin-top: 8px;
  padding: 10px 12px;
  background: #f8fafc;
  border-left: 3px solid #cbd5e1;
  border-radius: 0 6px 6px 0;
  font-size: 12px;
  font-style: italic;
  color: #475569;
  line-height: 1.4;
}

/* Responsive */
@media (max-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  .left-sidebar {
    display: none;
  }
}
</style>
