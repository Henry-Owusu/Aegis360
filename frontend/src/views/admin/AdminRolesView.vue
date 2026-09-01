<script setup lang="ts">
import { ref } from 'vue'
import AdminLayout from './components/AdminLayout.vue'

// ─── Mock Data ────────────────────────────────────────────────────────────────

const roles = ref([
  {
    id: 'r1',
    name: 'System Administrator',
    description: 'Full system administration access across all modules',
    userCount: 3,
    permissionsCount: 24,
    type: 'core',
  },
  {
    id: 'r2',
    name: 'DPO',
    description: 'Data Protection Officer responsible for compliance and reviews',
    userCount: 2,
    permissionsCount: 18,
    type: 'custom',
  },
  {
    id: 'r3',
    name: 'PM',
    description: 'Project Manager responsible for creating and submitting DPIAs',
    userCount: 15,
    permissionsCount: 12,
    type: 'custom',
  },
  {
    id: 'r4',
    name: 'Approver',
    description: 'Legal or senior approval authority for assessments',
    userCount: 8,
    permissionsCount: 6,
    type: 'custom',
  },
  {
    id: 'r5',
    name: 'Auditor',
    description: 'Read-only access for external or internal auditing',
    userCount: 4,
    permissionsCount: 8,
    type: 'custom',
  },
])

const searchQuery = ref('')
</script>

<template>
  <AdminLayout>
    <div class="page-header">
      <div>
        <h2 class="page-title">Role Management</h2>
        <p class="page-sub">Define and manage user roles and their associated permissions</p>
      </div>
      <button class="btn-primary">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        Create Role
      </button>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <div class="search-box">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input v-model="searchQuery" type="text" placeholder="Search roles..." />
      </div>
    </div>

    <!-- Roles Grid -->
    <div class="roles-grid">
      <div v-for="role in roles" :key="role.id" class="role-card">
        <div class="card-header">
          <div class="title-group">
            <h3 class="role-name">{{ role.name }}</h3>
            <span v-if="role.type === 'core'" class="badge-core">Core Role</span>
          </div>
          <button class="more-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="1"></circle>
              <circle cx="19" cy="12" r="1"></circle>
              <circle cx="5" cy="12" r="1"></circle>
            </svg>
          </button>
        </div>

        <p class="role-desc">{{ role.description }}</p>

        <div class="role-stats">
          <div class="stat">
            <div class="stat-val">{{ role.userCount }}</div>
            <div class="stat-lbl">Assigned Users</div>
          </div>
          <div class="stat">
            <div class="stat-val">{{ role.permissionsCount }}</div>
            <div class="stat-lbl">Permissions</div>
          </div>
        </div>

        <div class="card-footer">
          <button class="action-link">Edit Permissions</button>
          <button class="action-link outline">View Users</button>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

<style scoped>
/* ── Page Header ─────────────────────────────────────────────── */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}
.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #ffffff;
  margin: 0 0 6px;
}
.page-sub {
  color: #92929d;
  font-size: 14px;
  margin: 0;
}
.btn-primary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 12px;
  background: linear-gradient(135deg, #fdba74, #f58425);
  border: none;
  color: #ffffff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}
.btn-primary svg {
  width: 16px;
  height: 16px;
}
.btn-primary:hover {
  opacity: 0.9;
}

/* ── Toolbar ─────────────────────────────────────────────────── */
.toolbar {
  display: flex;
  margin-bottom: 24px;
}
.search-box {
  flex: 1;
  max-width: 400px;
  display: flex;
  align-items: center;
  gap: 10px;
  background: #1c1c24;
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  padding: 0 16px;
}
.search-box svg {
  width: 18px;
  height: 18px;
  color: #92929d;
  flex-shrink: 0;
}
.search-box input {
  background: transparent;
  border: none;
  color: #ffffff;
  font-size: 14px;
  outline: none;
  width: 100%;
  padding: 12px 0;
}
.search-box input::placeholder {
  color: #92929d;
}

/* ── Roles Grid ──────────────────────────────────────────────── */
.roles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
}
.role-card {
  background: #1c1c24;
  border-radius: 20px;
  padding: 24px;
  border: 1px solid rgba(255, 255, 255, 0.04);
  display: flex;
  flex-direction: column;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}
.title-group {
  display: flex;
  align-items: center;
  gap: 10px;
}
.role-name {
  font-size: 18px;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
}
.badge-core {
  background: rgba(245, 132, 37, 0.12);
  color: #fdba74;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.more-btn {
  background: none;
  border: none;
  color: #92929d;
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  transition: all 0.2s;
}
.more-btn:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.05);
}
.more-btn svg {
  width: 16px;
  height: 16px;
}

.role-desc {
  color: #92929d;
  font-size: 14px;
  line-height: 1.5;
  margin: 0 0 24px;
  flex: 1;
}

.role-stats {
  display: flex;
  gap: 32px;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}
.stat-val {
  font-size: 20px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 4px;
}
.stat-lbl {
  font-size: 12px;
  color: #92929d;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.card-footer {
  display: flex;
  gap: 12px;
}
.action-link {
  flex: 1;
  background: rgba(245, 132, 37, 0.12);
  color: #f58425;
  border: none;
  padding: 10px 0;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.action-link:hover {
  background: rgba(245, 132, 37, 0.2);
}
.action-link.outline {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #e2e8f0;
}
.action-link.outline:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.2);
}
</style>
