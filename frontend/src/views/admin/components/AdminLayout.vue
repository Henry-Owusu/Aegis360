<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AdminSidebar from './AdminSidebar.vue'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="admin-dark-layout">
    <!-- Left Sidebar -->
    <AdminSidebar />

    <!-- Main Content Area Wrapper -->
    <div class="content-wrapper">
      <!-- Top Navbar -->
      <header class="top-navbar">
        <div class="navbar-left">
          <div class="search-bar">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <input type="text" placeholder="Search your needs" class="search-input" />
          </div>
        </div>

        <div class="navbar-actions">
          <button type="button" class="action-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="7 10 12 15 17 10"></polyline>
              <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
            <span>Export report</span>
          </button>

          <button type="button" class="icon-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
              <polyline points="22,6 12,13 2,6"></polyline>
            </svg>
            <span class="badge green">2</span>
          </button>

          <button type="button" class="icon-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
            <span class="badge yellow">3</span>
          </button>

          <div class="user-profile" @click="handleLogout" title="Sign Out">
            <div class="avatar">
              <img :src="authStore.user.avatar" :alt="authStore.user.name" />
            </div>
            <div class="user-info">
              <span class="name">{{ authStore.user.name }}</span>
              <span class="role">{{ authStore.user.role }}</span>
            </div>
            <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </div>
        </div>
      </header>

      <!-- Page Content Slot -->
      <main class="main-content">
        <slot></slot>
      </main>
    </div>
  </div>
</template>

<style scoped>
.admin-dark-layout {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background-color: #13131A;
  color: #FFFFFF;
  font-family: 'Inter', system-ui, sans-serif;
}

.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.top-navbar {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  background-color: #13131A;
}

.search-bar {
  display: flex;
  align-items: center;
  background-color: #1C1C24;
  border-radius: 999px;
  padding: 10px 16px;
  width: 320px;
}

.search-icon {
  width: 18px;
  height: 18px;
  color: #92929D;
  margin-right: 12px;
}

.search-input {
  background: transparent;
  border: none;
  color: #FFFFFF;
  font-size: 14px;
  width: 100%;
  outline: none;
}

.search-input::placeholder {
  color: #92929D;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 24px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: transparent;
  border: none;
  color: #92929D;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s;
}

.action-btn:hover {
  color: #FFFFFF;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.icon-btn {
  position: relative;
  background: transparent;
  border: none;
  color: #92929D;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s;
}

.icon-btn:hover {
  color: #FFFFFF;
}

.icon-btn svg {
  width: 22px;
  height: 22px;
}

.badge {
  position: absolute;
  top: 0;
  right: 0;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  font-size: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #FFFFFF;
  border: 2px solid #13131A;
}

.badge.green {
  background-color: #22C55E;
}

.badge.yellow {
  background-color: #F59E0B;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding-left: 12px;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.name {
  font-size: 13.5px;
  font-weight: 600;
  color: #FFFFFF;
}

.role {
  font-size: 11px;
  color: #92929D;
  margin-top: 2px;
}

.chevron {
  width: 16px;
  height: 16px;
  color: #E29A46;
}

.main-content {
  flex: 1;
  padding: 0 40px 40px 40px;
  overflow-y: auto;
}
</style>
