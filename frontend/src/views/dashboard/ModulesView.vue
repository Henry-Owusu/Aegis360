<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const searchQuery = ref('')

const handleDpiaClick = () => {
  const role = authStore.primaryRole
  if (role === 'DPO') {
    router.push('/dpo/dashboard')
  } else if (role === 'PM') {
    router.push('/pm/dashboard')
  } else if (role === 'System Administrator') {
    router.push('/admin/dashboard')
  } else {
    router.push('/modules')
  }
}

const handleAdminClick = () => {
  router.push('/admin')
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="modules-layout">
    <!-- Top Header Navigation Bar -->
    <header class="top-navbar">
      <!-- Left Logo Section -->
      <div class="navbar-brand">
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
            placeholder="Search ERP data, assessments, DPIAs..."
            class="search-input"
          />
        </div>
      </div>

      <!-- Right Action & Profile Section -->
      <div class="navbar-actions">
        <!-- Notification Bell with Active Badge -->
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
            <span class="user-role">{{ authStore.primaryRole }}</span>
          </div>
          <div class="avatar-container">
            <img :src="authStore.user.avatar" :alt="authStore.user.name" class="user-avatar" />
          </div>
        </div>
      </div>
    </header>

    <!-- Main Body Workspace -->
    <div class="body-container">
      <!-- Main Content Area -->
      <main class="main-content">
        <!-- Page Welcome Hero Header -->
        <header class="page-hero">
          <div class="hero-text">
            <h1 class="hero-title">Select Assessment Module</h1>
            <p class="hero-subtitle">
              Launch data privacy, impact assessment, and system governance workflows for your enterprise ecosystem.
            </p>
          </div>
        </header>

        <!-- Modules Grid -->
        <section class="modules-grid-section">
          <div class="modules-grid">
            <!-- Featured Primary DPIA Assessment Module Card -->
            <div class="module-card dpia-card" @click="handleDpiaClick">
              <div class="corner-ribbon"></div>

              <div class="card-inner">
                <div class="card-top-row">
                  <div class="module-badge">
                    <svg class="shield-badge-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                      <polyline points="9 12 11 14 15 10"></polyline>
                    </svg>
                    <span>ACTIVE MODULE</span>
                  </div>
                </div>

                <div class="card-body-content">
                  <h2 class="module-title">DPIA Assessment</h2>
                  <p class="module-desc">
                    Data Protection Impact Assessment module for evaluating data privacy risks, compliance obligations, and risk mitigation measures.
                  </p>
                </div>

                <div class="card-action-bar">
                  <span class="action-text">Launch Module</span>
                  <svg class="action-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                    <polyline points="12 5 19 12 12 19"></polyline>
                  </svg>
                </div>
              </div>
            </div>

            <!-- Active System Administration Module Card -->
            <div v-if="authStore.primaryRole === 'System Administrator'" class="module-card admin-card" @click="handleAdminClick">
              <div class="corner-ribbon admin-ribbon"></div>

              <div class="card-inner">
                <div class="card-top-row">
                  <div class="module-badge admin-badge">
                    <svg class="shield-badge-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="3"></circle>
                      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
                    </svg>
                    <span>ADMIN MODULE</span>
                  </div>
                </div>

                <div class="card-body-content">
                  <h2 class="module-title">System Administration</h2>
                  <p class="module-desc">
                    Manage enterprise user accounts, RBAC permissions, security audit trails, and global GRC settings.
                  </p>
                </div>

                <div class="card-action-bar">
                  <span class="action-text">Launch Admin Suite</span>
                  <svg class="action-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                    <polyline points="12 5 19 12 12 19"></polyline>
                  </svg>
                </div>
              </div>
            </div>            <!-- VAPT Assessment Coming Soon Card -->
            <div class="module-card placeholder-card">
              <div class="corner-ribbon muted"></div>
              <div class="card-inner">
                <div class="card-top-row">
                  <div class="lock-tag">
                    <svg class="lock-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                      <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                    </svg>
                    <span>COMING SOON</span>
                  </div>
                </div>
                <div class="card-body-content">
                  <h2 class="module-title placeholder-title">VAPT Assessment</h2>
                  <p class="module-desc placeholder-desc">
                    Vulnerability Assessment and Penetration Testing security evaluation module.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<style scoped>
.modules-layout {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f8fafc;
}

/* Top Header Navbar */
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
  box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03);
}

.navbar-brand {
  display: flex;
  align-items: center;
}

.brand-logo-img {
  height: 90px;
  width: auto;
  object-fit: contain;
  filter: drop-shadow(0 2px 6px rgba(0, 0, 0, 0.04));
  transition: transform 0.2s ease;
}

.brand-logo-img:hover {
  transform: scale(1.02);
}

/* Search Bar */
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
  transition: all 0.2s ease;
}

.search-input::placeholder {
  color: #94a3b8;
}

.search-input:focus {
  background-color: #ffffff;
  border-color: #cbd5e1;
  box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.12);
}

/* Navbar Actions & Profile */
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
  transition: all 0.15s ease;
}

.notification-btn:hover {
  background-color: #ffffff;
  color: #0f172a;
  border-color: #cbd5e1;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
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
  border: 1px solid transparent;
  transition: all 0.15s ease;
}

.user-profile-menu:hover {
  background-color: #f1f5f9;
  border-color: #e2e8f0;
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
  line-height: 1.2;
}

.user-role {
  font-size: 11.5px;
  color: #64748b;
  line-height: 1.2;
  margin-top: 2px;
}

.avatar-container {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #e2e8f0;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.06);
}

.user-avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Body Layout */
.body-container {
  flex: 1;
  display: flex;
}

/* Main Content Workspace */
.main-content {
  flex: 1;
  padding: 40px 48px;
  background-color: #f8fafc;
  overflow-y: auto;
}

/* Hero Header */
.page-hero {
  margin-bottom: 36px;
  padding-bottom: 24px;
  border-bottom: 1px solid #e2e8f0;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  background-color: #e0f2fe;
  color: #0369a1;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
  margin-bottom: 10px;
}

.badge-icon {
  width: 13px;
  height: 13px;
}

.hero-title {
  font-family: var(--font-family);
  font-size: 26px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.02em;
}

.hero-subtitle {
  font-size: 14px;
  color: #64748b;
  margin-top: 6px;
  max-width: 560px;
}

/* Modules Grid Section */
.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 360px));
  gap: 28px;
}

/* Module Cards */
.module-card {
  position: relative;
  min-height: 230px;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px -8px rgba(15, 23, 42, 0.08);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Active DPIA Card */
.dpia-card {
  background: linear-gradient(135deg, #44b868 0%, #2e8b4e 100%);
  cursor: pointer;
}

.dpia-card:hover {
  transform: translateY(-6px) scale(1.01);
  box-shadow: 0 25px 40px -10px rgba(46, 139, 78, 0.4);
}

/* Active System Administration Card */
.admin-card {
  background: linear-gradient(135deg, #0f2942 0%, #030712 100%);
  cursor: pointer;
}

.admin-card:hover {
  transform: translateY(-6px) scale(1.01);
  box-shadow: 0 25px 40px -10px rgba(15, 41, 66, 0.5);
}

.admin-badge {
  background-color: rgba(255, 255, 255, 0.15) !important;
  color: #ffffff !important;
  backdrop-filter: blur(4px);
}

.card-inner {
  height: 100%;
  padding: 28px 28px 24px 28px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
  z-index: 2;
}

.card-top-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.module-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.22);
  backdrop-filter: blur(8px);
  padding: 4px 10px;
  border-radius: 9999px;
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #ffffff;
}

.shield-badge-icon {
  width: 13px;
  height: 13px;
}

/* Folded Corner Ribbon Accent */
.corner-ribbon {
  position: absolute;
  top: 0;
  right: 0;
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.96);
  clip-path: polygon(0 0, 100% 0, 100% 100%, 30% 100%, 0 30%);
  border-bottom-left-radius: 18px;
  box-shadow: -3px 3px 8px rgba(0, 0, 0, 0.12);
  z-index: 3;
}

.corner-ribbon.muted {
  background: rgba(241, 245, 249, 0.9);
}

.card-body-content {
  margin: 16px 0;
}

.module-title {
  font-family: var(--font-family);
  font-size: 22px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 8px;
}

.module-desc {
  font-size: 13px;
  color: rgba(255, 255, 255, 0.9);
  line-height: 1.5;
}

.card-action-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 14px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  color: #ffffff;
  font-size: 14px;
  font-weight: 600;
}

.action-arrow {
  width: 18px;
  height: 18px;
  transition: transform 0.2s ease;
}

.dpia-card:hover .action-arrow {
  transform: translateX(4px);
}

/* Wireframe Placeholder Cards */
.placeholder-card {
  background: #ffffff;
  border: 1px dashed #cbd5e1;
  box-shadow: none;
  opacity: 0.75;
}

.lock-tag {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: #f1f5f9;
  padding: 4px 10px;
  border-radius: 9999px;
  font-size: 10px;
  font-weight: 700;
  color: #64748b;
  letter-spacing: 0.05em;
}

.lock-icon {
  width: 12px;
  height: 12px;
}

.placeholder-title {
  color: #334155;
}

.placeholder-desc {
  color: #94a3b8;
}

/* Responsive */
@media (max-width: 768px) {
  .search-container {
    display: none;
  }
  .main-content {
    padding: 24px 20px;
  }
}
</style>
