<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const isActive = (path: string) => route.path === path || route.path.startsWith(path + '/')
</script>

<template>
  <aside class="left-sidebar">
    <div class="sidebar-group">
      <h3 class="group-title">CORE OPERATIONS</h3>
      <nav class="sidebar-nav">
        <button
          type="button"
          class="nav-btn"
          :class="{ active: isActive('/pm/dashboard') }"
          @click="router.push('/pm/dashboard')"
        >
          <svg
            class="nav-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect x="3" y="3" width="7" height="7"></rect>
            <rect x="14" y="3" width="7" height="7"></rect>
            <rect x="14" y="14" width="7" height="7"></rect>
            <rect x="3" y="14" width="7" height="7"></rect>
          </svg>
          <span>Dashboard</span>
        </button>

        <button
          type="button"
          class="nav-btn"
          :class="{ active: isActive('/pm/dpias') || route.path === '/pm/dpia/new' }"
          @click="router.push('/pm/dpias')"
        >
          <svg
            class="nav-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
          </svg>
          <span>DPIA Module</span>
        </button>

        <button
          type="button"
          class="nav-btn"
          :class="{ active: isActive('/pm/risk-register') }"
          @click="router.push('/pm/risk-register')"
        >
          <svg
            class="nav-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
          </svg>
          <span>Risk Register</span>
        </button>

        <button
          type="button"
          class="nav-btn"
          :class="{ active: isActive('/pm/reports') }"
          @click="router.push('/pm/reports')"
        >
          <svg
            class="nav-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <line x1="18" y1="20" x2="18" y2="10"></line>
            <line x1="12" y1="20" x2="12" y2="4"></line>
            <line x1="6" y1="20" x2="6" y2="14"></line>
          </svg>
          <span>Reports</span>
        </button>
      </nav>
    </div>
  </aside>
</template>

<style scoped>
.left-sidebar {
  width: 240px;
  background-color: #ffffff;
  border-right: 1px solid #e2e8f0;
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  gap: 28px;
  height: 100%;
}

.sidebar-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.group-title {
  font-size: 11px;
  font-weight: 700;
  color: #64748b;
  letter-spacing: 0.08em;
  padding: 0 12px;
  margin-bottom: 4px;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 10px 14px;
  background: transparent;
  border: none;
  border-radius: 8px;
  font-family: var(--font-family);
  font-size: 13.5px;
  font-weight: 500;
  color: #475569;
  cursor: pointer;
  transition: all 0.15s ease;
  text-align: left;
}

.nav-btn:hover {
  background-color: #f8fafc;
  color: #0f172a;
}

.nav-btn.active {
  background-color: #0f2942;
  color: #ffffff;
  font-weight: 600;
}

.nav-icon {
  width: 17px;
  height: 17px;
}
</style>
