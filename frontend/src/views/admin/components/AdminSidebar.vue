<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const isActive = (path: string) => route.path === path || route.path.startsWith(path + '/')
</script>

<template>
  <aside class="dark-sidebar">
    <div class="sidebar-header">
      <div class="brand">
        <img src="/Aegislogo_no_bg.png" alt="Aegis360 Logo" class="brand-logo" />
      </div>
      <div class="store-selector">
        <span>Admin Suite</span>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="6 9 12 15 18 9"></polyline>
        </svg>
      </div>
    </div>

    <div class="sidebar-scroll">
      <nav class="sidebar-nav">
        <!-- Dashboard -->
        <button
          type="button"
          class="nav-btn"
          :class="{ active: isActive('/admin/dashboard') }"
          @click="router.push('/admin/dashboard')"
        >
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7" rx="1.5"></rect>
            <rect x="14" y="3" width="7" height="7" rx="1.5"></rect>
            <rect x="14" y="14" width="7" height="7" rx="1.5"></rect>
            <rect x="3" y="14" width="7" height="7" rx="1.5"></rect>
          </svg>
          <span>Dashboard</span>
        </button>

        <!-- Users -->
        <button
          type="button"
          class="nav-btn"
          :class="{ active: isActive('/admin/users') }"
          @click="router.push('/admin/users')"
        >
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          <span>Users</span>
        </button>

        <!-- Assessments -->
        <button
          type="button"
          class="nav-btn"
          :class="{ active: isActive('/admin/assessments') }"
          @click="router.push('/admin/assessments')"
        >
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
          </svg>
          <span>Assessments</span>
        </button>

        <!-- Modules -->
        <button
          type="button"
          class="nav-btn"
          :class="{ active: isActive('/admin/modules') }"
          @click="router.push('/admin/modules')"
        >
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
          </svg>
          <span>Modules</span>
        </button>

        <!-- Questions -->
        <button
          type="button"
          class="nav-btn"
          :class="{ active: isActive('/admin/questions') }"
          @click="router.push('/admin/questions')"
        >
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
          </svg>
          <span>Questions</span>
        </button>

        <!-- Roles -->
        <button
          type="button"
          class="nav-btn"
          :class="{ active: isActive('/admin/roles') }"
          @click="router.push('/admin/roles')"
        >
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
          </svg>
          <span>Roles</span>
        </button>

        <!-- Permissions -->
        <button
          type="button"
          class="nav-btn"
          :class="{ active: isActive('/admin/permissions') }"
          @click="router.push('/admin/permissions')"
        >
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          <span>Permissions</span>
        </button>
      </nav>

      <div class="sidebar-bottom">
        <nav class="sidebar-nav">
          <button
            type="button"
            class="nav-btn"
            :class="{ active: isActive('/admin/settings') }"
            @click="router.push('/admin/settings')"
          >
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
            <span>Settings</span>
          </button>
          
          <button 
            type="button" 
            class="nav-btn"
            :class="{ active: isActive('/admin/help') }"
            @click="router.push('/admin/help')"
          >
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            <span>Help Center</span>
          </button>
        </nav>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.dark-sidebar {
  width: 250px;
  background-color: #13131A;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.sidebar-header {
  padding: 32px 24px 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-logo {
  height: 105px;
  width: auto;
  object-fit: contain;
  filter: brightness(1.7);
}

.store-selector {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #1C1C24;
  padding: 12px 16px;
  border-radius: 12px;
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.store-selector span {
  font-size: 13px;
  font-weight: 500;
  color: #92929D;
}

.store-selector svg {
  width: 16px;
  height: 16px;
  color: #92929D;
}

.sidebar-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 0 16px;
  display: flex;
  flex-direction: column;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.sidebar-bottom {
  margin-top: auto;
  padding-top: 32px;
  padding-bottom: 24px;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 16px;
  width: 100%;
  padding: 14px 20px;
  background: transparent;
  border: none;
  border-radius: 14px;
  font-family: var(--font-family);
  font-size: 14px;
  font-weight: 500;
  color: #92929D;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: left;
}

.nav-btn:hover {
  color: #FFFFFF;
}

.nav-btn.active {
  background: linear-gradient(135deg, #FDBA74 0%, #F58425 100%);
  color: #FFFFFF;
  font-weight: 600;
  box-shadow: 0 8px 16px rgba(245, 132, 37, 0.25);
}

.nav-icon {
  width: 20px;
  height: 20px;
}

.nav-btn.active .nav-icon {
  stroke-width: 2.5;
}
</style>
