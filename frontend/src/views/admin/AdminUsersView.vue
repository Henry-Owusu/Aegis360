<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminLayout from './components/AdminLayout.vue'
import { usersApi, type UserRecord, type RoleRecord } from '@/services/api'

// ─── State ────────────────────────────────────────────────────────────────────

const users = ref<UserRecord[]>([])
const roles = ref<RoleRecord[]>([])
const isLoading = ref(true)
const searchQuery = ref('')
const filterRole = ref('all')
const filterStatus = ref('all')

// Modal state
const showAssignModal = ref(false)
const selectedUser = ref<UserRecord | null>(null)
const selectedRole = ref('')
const isSubmitting = ref(false)
const toastMessage = ref('')
const toastType = ref<'success' | 'error'>('success')

// ─── Computed ─────────────────────────────────────────────────────────────────

const filteredUsers = computed(() => {
  return users.value.filter((u) => {
    const matchesSearch =
      !searchQuery.value ||
      `${u.first_name} ${u.last_name}`.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      u.email.toLowerCase().includes(searchQuery.value.toLowerCase())

    const matchesRole = filterRole.value === 'all' || u.roles.includes(filterRole.value)

    const matchesStatus =
      filterStatus.value === 'all' ||
      (filterStatus.value === 'active' && u.is_active) ||
      (filterStatus.value === 'inactive' && !u.is_active)

    return matchesSearch && matchesRole && matchesStatus
  })
})

const totalActive = computed(() => users.value.filter((u) => u.is_active).length)
const totalInactive = computed(() => users.value.filter((u) => !u.is_active).length)

// ─── Actions ──────────────────────────────────────────────────────────────────

const fetchData = async () => {
  isLoading.value = true
  try {
    const [usersRes, rolesRes] = await Promise.all([usersApi.listUsers(), usersApi.listRoles()])
    users.value = usersRes.users
    roles.value = rolesRes.roles
  } catch (err) {
    showToast('Failed to load users', 'error')
  } finally {
    isLoading.value = false
  }
}

const toggleStatus = async (user: UserRecord) => {
  try {
    const res = await usersApi.toggleStatus(user.id)
    user.is_active = res.is_active
    showToast(res.message, 'success')
  } catch (err: unknown) {
    showToast(err instanceof Error ? err.message : 'Failed to update status', 'error')
  }
}

const openAssignModal = (user: UserRecord) => {
  selectedUser.value = user
  selectedRole.value = ''
  showAssignModal.value = true
}

const assignRole = async () => {
  if (!selectedUser.value || !selectedRole.value) return
  isSubmitting.value = true
  try {
    const res = await usersApi.assignRole(selectedUser.value.id, selectedRole.value)
    selectedUser.value.roles = res.roles
    showToast(`Role assigned successfully`, 'success')
    showAssignModal.value = false
  } catch (err: unknown) {
    showToast(err instanceof Error ? err.message : 'Failed to assign role', 'error')
  } finally {
    isSubmitting.value = false
  }
}

const removeRole = async (user: UserRecord, roleName: string) => {
  try {
    const res = await usersApi.removeRole(user.id, roleName)
    user.roles = res.roles
    showToast(`Role removed`, 'success')
  } catch (err: unknown) {
    showToast(err instanceof Error ? err.message : 'Failed to remove role', 'error')
  }
}

const showToast = (message: string, type: 'success' | 'error') => {
  toastMessage.value = message
  toastType.value = type
  setTimeout(() => {
    toastMessage.value = ''
  }, 3500)
}

const initials = (u: UserRecord) => `${u.first_name[0] ?? ''}${u.last_name[0] ?? ''}`.toUpperCase()

const formatDate = (iso: string) =>
  new Date(iso).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })

onMounted(fetchData)
</script>

<template>
  <AdminLayout>
    <!-- Toast Notification -->
    <Transition name="toast">
      <div v-if="toastMessage" class="toast" :class="toastType">
        <svg
          v-if="toastType === 'success'"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.5"
        >
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <span>{{ toastMessage }}</span>
      </div>
    </Transition>

    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h2 class="page-title">User Management</h2>
        <p class="page-sub">Manage system users, roles and access permissions</p>
      </div>
      <div class="header-stats">
        <div class="stat-chip green">
          <span class="dot"></span>
          {{ totalActive }} Active
        </div>
        <div class="stat-chip red">
          <span class="dot"></span>
          {{ totalInactive }} Inactive
        </div>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="toolbar">
      <div class="search-box">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input v-model="searchQuery" type="text" placeholder="Search by name or email..." />
      </div>
      <div class="filters">
        <select v-model="filterRole" class="filter-select">
          <option value="all">All Roles</option>
          <option v-for="r in roles" :key="r.id" :value="r.name">{{ r.name }}</option>
        </select>
        <select v-model="filterStatus" class="filter-select">
          <option value="all">All Status</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state">
      <div class="spinner-ring"></div>
      <p>Loading users...</p>
    </div>

    <!-- Users Table -->
    <div v-else class="table-card">
      <table class="users-table">
        <thead>
          <tr>
            <th>User</th>
            <th>Roles</th>
            <th>Status</th>
            <th>Joined</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredUsers.length === 0">
            <td colspan="5" class="empty-row">No users match your filters</td>
          </tr>
          <tr v-for="user in filteredUsers" :key="user.id">
            <!-- User Info -->
            <td class="user-cell">
              <div class="avatar-initials">{{ initials(user) }}</div>
              <div class="user-info">
                <span class="user-name">{{ user.first_name }} {{ user.last_name }}</span>
                <span class="user-email">{{ user.email }}</span>
              </div>
            </td>

            <!-- Roles -->
            <td class="roles-cell">
              <div class="role-tags">
                <span v-for="role in user.roles" :key="role" class="role-tag">
                  {{ role }}
                  <button
                    class="remove-role-btn"
                    @click="removeRole(user, role)"
                    title="Remove role"
                  >
                    ×
                  </button>
                </span>
                <span v-if="user.roles.length === 0" class="no-role">No role</span>
                <button class="add-role-btn" @click="openAssignModal(user)" title="Assign role">
                  +
                </button>
              </div>
            </td>

            <!-- Status -->
            <td>
              <span class="status-badge" :class="user.is_active ? 'active' : 'inactive'">
                <span class="status-dot"></span>
                {{ user.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>

            <!-- Date -->
            <td class="date-cell">{{ formatDate(user.created_at) }}</td>

            <!-- Actions -->
            <td class="actions-cell">
              <button
                class="action-toggle"
                :class="user.is_active ? 'deactivate' : 'activate'"
                @click="toggleStatus(user)"
              >
                {{ user.is_active ? 'Deactivate' : 'Activate' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Assign Role Modal -->
    <Transition name="modal">
      <div v-if="showAssignModal" class="modal-overlay" @click.self="showAssignModal = false">
        <div class="modal-card">
          <div class="modal-header">
            <h3>Assign Role</h3>
            <button class="modal-close" @click="showAssignModal = false">×</button>
          </div>
          <div class="modal-body">
            <p class="modal-sub">
              Assigning role to
              <strong>{{ selectedUser?.first_name }} {{ selectedUser?.last_name }}</strong>
            </p>
            <div class="current-roles">
              <span class="label">Current roles:</span>
              <span v-if="selectedUser?.roles.length === 0" class="no-role">None</span>
              <span v-for="r in selectedUser?.roles" :key="r" class="role-tag">{{ r }}</span>
            </div>
            <label class="field-label">Select Role</label>
            <select v-model="selectedRole" class="role-select">
              <option value="" disabled>Choose a role...</option>
              <option
                v-for="r in roles"
                :key="r.id"
                :value="r.name"
                :disabled="selectedUser?.roles.includes(r.name)"
              >
                {{ r.name }}{{ selectedUser?.roles.includes(r.name) ? ' (already assigned)' : '' }}
              </option>
            </select>
          </div>
          <div class="modal-footer">
            <button class="btn-cancel" @click="showAssignModal = false">Cancel</button>
            <button
              class="btn-assign"
              :disabled="!selectedRole || isSubmitting"
              @click="assignRole"
            >
              <span v-if="isSubmitting">Assigning...</span>
              <span v-else>Assign Role</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>
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
.header-stats {
  display: flex;
  gap: 12px;
}
.stat-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
}
.stat-chip.green {
  background: rgba(34, 197, 94, 0.12);
  color: #4ade80;
}
.stat-chip.red {
  background: rgba(239, 68, 68, 0.12);
  color: #f87171;
}
.dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: currentColor;
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
.filters {
  display: flex;
  gap: 12px;
}
.filter-select {
  background: #1c1c24;
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  color: #ffffff;
  font-size: 13px;
  padding: 10px 16px;
  outline: none;
  cursor: pointer;
}
.filter-select option {
  background: #1c1c24;
}

/* ── Loading ─────────────────────────────────────────────────── */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 80px 0;
  color: #92929d;
}
.spinner-ring {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(245, 132, 37, 0.2);
  border-top-color: #f58425;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* ── Table ───────────────────────────────────────────────────── */
.table-card {
  background: #1c1c24;
  border-radius: 20px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.04);
}
.users-table {
  width: 100%;
  border-collapse: collapse;
}
.users-table th {
  text-align: left;
  padding: 18px 20px;
  color: #92929d;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}
.users-table td {
  padding: 16px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
  vertical-align: middle;
}
.users-table tr:last-child td {
  border-bottom: none;
}
.users-table tr:hover td {
  background: rgba(255, 255, 255, 0.02);
}
.empty-row {
  text-align: center;
  color: #92929d;
  font-size: 14px;
  padding: 48px !important;
}

/* ── User Cell ───────────────────────────────────────────────── */
.user-cell {
  display: flex;
  align-items: center;
  gap: 14px;
}
.avatar-initials {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, #fdba74, #f58425);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
}
.user-info {
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #ffffff;
}
.user-email {
  font-size: 12px;
  color: #92929d;
}

/* ── Roles ───────────────────────────────────────────────────── */
.roles-cell {
  max-width: 240px;
}
.role-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
}
.role-tag {
  display: flex;
  align-items: center;
  gap: 4px;
  background: rgba(245, 132, 37, 0.12);
  color: #fdba74;
  border-radius: 20px;
  padding: 4px 10px 4px 12px;
  font-size: 12px;
  font-weight: 600;
}
.remove-role-btn {
  background: none;
  border: none;
  color: #fdba74;
  cursor: pointer;
  font-size: 16px;
  line-height: 1;
  padding: 0;
  opacity: 0.6;
  transition: opacity 0.15s;
}
.remove-role-btn:hover {
  opacity: 1;
}
.no-role {
  font-size: 12px;
  color: #4a4a57;
  font-style: italic;
}
.add-role-btn {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px dashed rgba(255, 255, 255, 0.15);
  color: #92929d;
  cursor: pointer;
  font-size: 18px;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}
.add-role-btn:hover {
  background: rgba(245, 132, 37, 0.15);
  color: #f58425;
  border-color: #f58425;
}

/* ── Status ──────────────────────────────────────────────────── */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}
.status-badge.active {
  background: rgba(34, 197, 94, 0.12);
  color: #4ade80;
}
.status-badge.inactive {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
}
.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

/* ── Date ────────────────────────────────────────────────────── */
.date-cell {
  color: #92929d;
  font-size: 13px;
}

/* ── Actions ─────────────────────────────────────────────────── */
.action-toggle {
  padding: 7px 16px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}
.action-toggle.deactivate {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
}
.action-toggle.deactivate:hover {
  background: rgba(239, 68, 68, 0.2);
}
.action-toggle.activate {
  background: rgba(34, 197, 94, 0.1);
  color: #4ade80;
}
.action-toggle.activate:hover {
  background: rgba(34, 197, 94, 0.2);
}

/* ── Toast ───────────────────────────────────────────────────── */
.toast {
  position: fixed;
  bottom: 32px;
  right: 32px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 20px;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 500;
  z-index: 1000;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}
.toast svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}
.toast.success {
  background: #1c2e22;
  color: #4ade80;
  border: 1px solid rgba(74, 222, 128, 0.2);
}
.toast.error {
  background: #2e1c1c;
  color: #f87171;
  border: 1px solid rgba(248, 113, 113, 0.2);
}
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(16px);
}

/* ── Modal ───────────────────────────────────────────────────── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 500;
  backdrop-filter: blur(4px);
}
.modal-card {
  background: #1c1c24;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  width: 440px;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.5);
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 28px 0;
}
.modal-header h3 {
  font-size: 18px;
  font-weight: 700;
  color: #ffffff;
}
.modal-close {
  background: none;
  border: none;
  color: #92929d;
  font-size: 24px;
  cursor: pointer;
  transition: color 0.2s;
}
.modal-close:hover {
  color: #ffffff;
}
.modal-body {
  padding: 20px 28px;
}
.modal-sub {
  color: #92929d;
  font-size: 14px;
  margin: 0 0 16px;
}
.modal-sub strong {
  color: #ffffff;
}
.current-roles {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
  margin-bottom: 20px;
}
.label {
  font-size: 12px;
  color: #92929d;
  margin-right: 4px;
}
.field-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #92929d;
  margin-bottom: 8px;
}
.role-select {
  width: 100%;
  background: #13131a;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  color: #ffffff;
  font-size: 14px;
  padding: 12px 16px;
  outline: none;
}
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 0 28px 24px;
}
.btn-cancel {
  padding: 10px 20px;
  border-radius: 10px;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #92929d;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-cancel:hover {
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.2);
}
.btn-assign {
  padding: 10px 24px;
  border-radius: 10px;
  background: linear-gradient(135deg, #fdba74, #f58425);
  border: none;
  color: #ffffff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}
.btn-assign:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.modal-enter-active,
.modal-leave-active {
  transition: all 0.25s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-from .modal-card,
.modal-leave-to .modal-card {
  transform: scale(0.95);
}
</style>
