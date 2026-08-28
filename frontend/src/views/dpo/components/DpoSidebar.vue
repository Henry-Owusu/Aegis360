<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import AegisLogo from '@/components/common/AegisLogo.vue'

const route = useRoute()
const router = useRouter()

const isActive = (path: string) => route.path === path

const handleNavigateModules = () => {
  router.push('/modules')
}
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar-header" @click="handleNavigateModules" style="cursor: pointer; justify-content: center;">
      <AegisLogo :height="42" />
    </div>

    <div class="sidebar-content">
      <div class="nav-section">
        <h3 class="nav-title">CORE OPERATIONS</h3>
        <nav class="nav-menu">
          <RouterLink to="/dpo/dashboard" class="nav-item" :class="{ active: isActive('/dpo/dashboard') }">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="3" y="3" width="7" height="7"></rect>
              <rect x="14" y="3" width="7" height="7"></rect>
              <rect x="14" y="14" width="7" height="7"></rect>
              <rect x="3" y="14" width="7" height="7"></rect>
            </svg>
            Dashboard
          </RouterLink>
          <RouterLink to="/dpo/dpias" class="nav-item" :class="{ active: isActive('/dpo/dpias') }">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            </svg>
            DPIA Module
          </RouterLink>
          <RouterLink to="/dpo/risk-register" class="nav-item" :class="{ active: isActive('/dpo/risk-register') }">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
              <polyline points="10 9 9 9 8 9"></polyline>
            </svg>
            Risk Register
          </RouterLink>
          <RouterLink to="/dpo/reports" class="nav-item" :class="{ active: isActive('/dpo/reports') }">
            <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="20" x2="18" y2="10"></line>
              <line x1="12" y1="20" x2="12" y2="4"></line>
              <line x1="6" y1="20" x2="6" y2="14"></line>
            </svg>
            Reports
          </RouterLink>
        </nav>
      </div>
    </div>
  </aside>
</template>

<style scoped>
/* Sidebar Styling */
.sidebar {
  width: 260px;
  background: #ffffff;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  height: 100%;
}

.sidebar-header {
  height: 72px;
  display: flex;
  align-items: center;
  padding: 0 24px;
  gap: 12px;
  border-bottom: 1px solid #e2e8f0;
}

.brand-name {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: 0.02em;
}

.sidebar-content {
  padding: 24px 16px;
  flex: 1;
  overflow-y: auto;
}

.nav-section {
  margin-bottom: 32px;
}

.nav-title {
  font-size: 11px;
  font-weight: 700;
  color: #94a3b8;
  letter-spacing: 0.08em;
  padding: 0 12px;
  margin-bottom: 12px;
  text-transform: uppercase;
}

.nav-menu {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 8px;
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
}

.nav-item:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.nav-item.active {
  background: #0f172a;
  color: #ffffff;
}

.nav-icon {
  width: 18px;
  height: 18px;
}
</style>
