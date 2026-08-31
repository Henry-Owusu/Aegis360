<script setup lang="ts">
import { ref } from 'vue'
import AdminLayout from './components/AdminLayout.vue'

// ─── Mock Data ────────────────────────────────────────────────────────────────

const permissions = ref([
  { id: 'p1', code: 'assessment.view', name: 'View Assessments', category: 'Assessments', roles: ['System Administrator', 'DPO', 'PM', 'Approver', 'Auditor'] },
  { id: 'p2', code: 'assessment.create', name: 'Create Assessments', category: 'Assessments', roles: ['System Administrator', 'PM'] },
  { id: 'p3', code: 'assessment.approve', name: 'Approve Assessments', category: 'Assessments', roles: ['System Administrator', 'Approver'] },
  { id: 'p4', code: 'user.view', name: 'View Users', category: 'User Management', roles: ['System Administrator'] },
  { id: 'p5', code: 'user.manage', name: 'Manage Users', category: 'User Management', roles: ['System Administrator'] },
  { id: 'p6', code: 'role.manage', name: 'Manage Roles', category: 'Access Control', roles: ['System Administrator'] },
  { id: 'p7', code: 'audit.view', name: 'View Audit Logs', category: 'System', roles: ['System Administrator', 'Auditor'] },
  { id: 'p8', code: 'settings.manage', name: 'Manage System Settings', category: 'System', roles: ['System Administrator'] }
])

const filterCategory = ref('all')
const searchQuery = ref('')
</script>

<template>
  <AdminLayout>
    <div class="page-header">
      <div>
        <h2 class="page-title">Permissions Directory</h2>
        <p class="page-sub">Comprehensive list of system permissions and role assignments</p>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <div class="search-box">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input v-model="searchQuery" type="text" placeholder="Search permissions by name or code..." />
      </div>
      <div class="filters">
        <select v-model="filterCategory" class="filter-select">
          <option value="all">All Categories</option>
          <option value="Assessments">Assessments</option>
          <option value="User Management">User Management</option>
          <option value="Access Control">Access Control</option>
          <option value="System">System</option>
        </select>
      </div>
    </div>

    <!-- Permissions Table -->
    <div class="table-card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Permission Name</th>
            <th>System Code</th>
            <th>Category</th>
            <th>Assigned Roles</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="perm in permissions" :key="perm.id">
            <td class="primary-cell">
              <span class="item-title">{{ perm.name }}</span>
            </td>
            <td>
              <code class="system-code">{{ perm.code }}</code>
            </td>
            <td>
              <span class="category-badge">{{ perm.category }}</span>
            </td>
            <td>
              <div class="role-tags">
                <span v-for="role in perm.roles" :key="role" class="role-tag">{{ role }}</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </AdminLayout>
</template>

<style scoped>
/* ── Page Header ─────────────────────────────────────────────── */
.page-header {
  margin-bottom: 32px;
}
.page-title {
  font-size: 24px;
  font-weight: 700;
  color: #FFFFFF;
  margin: 0 0 6px;
}
.page-sub {
  color: #92929D;
  font-size: 14px;
  margin: 0;
}

/* ── Toolbar ─────────────────────────────────────────────────── */
.toolbar {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}
.search-box {
  flex: 1;
  min-width: 260px;
  display: flex;
  align-items: center;
  gap: 10px;
  background: #1C1C24;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px;
  padding: 0 16px;
}
.search-box svg { width: 18px; height: 18px; color: #92929D; flex-shrink: 0; }
.search-box input {
  background: transparent;
  border: none;
  color: #FFFFFF;
  font-size: 14px;
  outline: none;
  width: 100%;
  padding: 12px 0;
}
.search-box input::placeholder { color: #92929D; }
.filters { display: flex; gap: 12px; }
.filter-select {
  background: #1C1C24;
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px;
  color: #FFFFFF;
  font-size: 13px;
  padding: 10px 16px;
  outline: none;
  cursor: pointer;
}

/* ── Table ───────────────────────────────────────────────────── */
.table-card {
  background: #1C1C24;
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.04);
}
.data-table {
  width: 100%;
  border-collapse: collapse;
}
.data-table th {
  text-align: left;
  padding: 18px 20px;
  color: #92929D;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  border-bottom: 1px solid rgba(255,255,255,0.04);
}
.data-table td {
  padding: 16px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.03);
  vertical-align: middle;
}
.data-table tr:last-child td { border-bottom: none; }
.data-table tr:hover td { background: rgba(255,255,255,0.02); }

/* ── Cells ───────────────────────────────────────────────────── */
.primary-cell { display: flex; flex-direction: column; gap: 4px; }
.item-title { font-size: 14px; font-weight: 600; color: #FFFFFF; }
.system-code {
  font-family: monospace; font-size: 13px;
  color: #FDBA74; background: rgba(245,132,37,0.08);
  padding: 4px 8px; border-radius: 6px; border: 1px solid rgba(245,132,37,0.15);
}
.category-badge {
  font-size: 12px; color: #E2E8F0; background: rgba(255,255,255,0.06);
  padding: 4px 10px; border-radius: 12px;
}
.role-tags {
  display: flex; flex-wrap: wrap; gap: 6px;
}
.role-tag {
  font-size: 11px; font-weight: 600; color: #94A3B8;
  border: 1px solid rgba(148,163,184,0.3); padding: 2px 8px;
  border-radius: 10px;
}
</style>
