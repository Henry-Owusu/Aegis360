<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const searchQuery = ref('')
const activeTab = ref<'users' | 'audit' | 'settings'>('users')

// Search & Filter state for Users
const userSearchQuery = ref('')
const selectedRoleFilter = ref('ALL')

// User Management Data
interface SystemUser {
  id: string
  name: string
  email: string
  role: string
  department: string
  authSource: string
  status: 'Active' | 'Inactive' | 'Pending'
  lastLogin: string
  avatar: string
}

const systemUsers = ref<SystemUser[]>([
  {
    id: 'USR-001',
    name: 'Executive Admin',
    email: 'admin@aegis360.io',
    role: 'Global Controller',
    department: 'Executive Governance',
    authSource: 'Microsoft Entra ID',
    status: 'Active',
    lastLogin: '2 mins ago',
    avatar:
      'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop&q=80',
  },
  {
    id: 'USR-002',
    name: 'Marcus Vance',
    email: 'marcus.vance@aegis360.io',
    role: 'Data Protection Officer',
    department: 'Legal & Privacy',
    authSource: 'Microsoft Entra ID',
    status: 'Active',
    lastLogin: '1 hour ago',
    avatar:
      'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop&q=80',
  },
  {
    id: 'USR-003',
    name: 'Elena Rostova',
    email: 'elena.rostova@aegis360.io',
    role: 'Senior Privacy Counsel',
    department: 'Legal & Compliance',
    authSource: 'Microsoft Entra ID',
    status: 'Active',
    lastLogin: '3 hours ago',
    avatar:
      'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=100&auto=format&fit=crop&q=80',
  },
  {
    id: 'USR-004',
    name: 'David Chen',
    email: 'david.chen@aegis360.io',
    role: 'Project Manager',
    department: 'Core Operations',
    authSource: 'Microsoft Entra ID',
    status: 'Active',
    lastLogin: 'Yesterday',
    avatar:
      'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&auto=format&fit=crop&q=80',
  },
  {
    id: 'USR-005',
    name: 'Sarah Jenkins',
    email: 'sarah.j@aegis360.io',
    role: 'Security Auditor',
    department: 'InfoSec Audit',
    authSource: 'Microsoft Entra ID',
    status: 'Pending',
    lastLogin: 'Never',
    avatar:
      'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&auto=format&fit=crop&q=80',
  },
])

const filteredUsers = computed(() => {
  return systemUsers.value.filter((u) => {
    const matchesSearch =
      u.name.toLowerCase().includes(userSearchQuery.value.toLowerCase()) ||
      u.email.toLowerCase().includes(userSearchQuery.value.toLowerCase()) ||
      u.department.toLowerCase().includes(userSearchQuery.value.toLowerCase())
    const matchesRole = selectedRoleFilter.value === 'ALL' || u.role === selectedRoleFilter.value
    return matchesSearch && matchesRole
  })
})

// System Audit Logs Data
interface AuditLog {
  id: string
  timestamp: string
  user: string
  action: string
  module: string
  ipAddress: string
  severity: 'Critical' | 'Warning' | 'Info'
}

const auditLogs = ref<AuditLog[]>([
  {
    id: 'LOG-8802',
    timestamp: '2026-08-27 16:45:12',
    user: 'Executive Admin',
    action: 'Modified Risk Matrix Screening Thresholds',
    module: 'DPIA Engine',
    ipAddress: '192.168.1.104',
    severity: 'Warning',
  },
  {
    id: 'LOG-8801',
    timestamp: '2026-08-27 16:22:04',
    user: 'Marcus Vance',
    action: 'Approved DPIA Assessment for Project Phoenix',
    module: 'DPIA Module',
    ipAddress: '10.0.4.12',
    severity: 'Info',
  },
  {
    id: 'LOG-8800',
    timestamp: '2026-08-27 15:58:30',
    user: 'System Process',
    action: 'Microsoft Entra ID SSO Token Renewal Success',
    module: 'Authentication',
    ipAddress: 'Internal System',
    severity: 'Info',
  },
  {
    id: 'LOG-8799',
    timestamp: '2026-08-27 14:12:45',
    user: 'David Chen',
    action: 'Failed Login Attempt (MFA Invalid Token)',
    module: 'Authentication',
    ipAddress: '198.51.100.42',
    severity: 'Critical',
  },
])

// System Configuration State
const entraTenantId = ref('72f988bf-86f1-41af-91ab-2d7cd011db47')
const entraClientId = ref('aegis360-entra-sso-app-prod')
const dpiaThreshold = ref(60)
const autoDpoAssignment = ref(true)
const auditLogRetentionDays = ref(365)

const handleSaveSettings = () => {
  window.alert('System Configuration updated successfully!')
}

const handleAddUser = () => {
  window.alert('Opening Entra ID User Provisioning Modal...')
}

const handleNavigateModules = () => {
  router.push('/modules')
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <div class="admin-layout">
    <!-- Top Header Navigation Bar -->
    <header class="top-navbar">
      <div class="navbar-brand" @click="handleNavigateModules" title="Back to Modules">
        <img src="/Aegislogo.jpeg" alt="Aegis360 Logo" class="brand-logo-img" />
      </div>

      <div class="search-container">
        <div class="search-input-wrapper">
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
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search ERP data..."
            class="search-input"
          />
        </div>
      </div>

      <div class="navbar-actions">
        <button type="button" class="notification-btn" title="Notifications">
          <svg
            class="bell-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
            <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
          </svg>
          <span class="notification-dot"></span>
        </button>

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

    <!-- Main Container with Left Sidebar & Admin Workspace -->
    <div class="body-container">
      <!-- Left Sidebar Navigation -->
      <aside class="left-sidebar">
        <div class="sidebar-group">
          <h3 class="group-title">CORE OPERATIONS</h3>
          <nav class="sidebar-nav">
            <button type="button" class="nav-btn" @click="router.push('/dpia')">
              <svg
                class="nav-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <rect x="3" y="3" width="7" height="7"></rect>
                <rect x="14" y="3" width="7" height="7"></rect>
                <rect x="14" y="14" width="7" height="7"></rect>
                <rect x="3" y="14" width="7" height="7"></rect>
              </svg>
              <span>Dashboard</span>
            </button>

            <button type="button" class="nav-btn" @click="router.push('/dpia/new')">
              <svg
                class="nav-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
              </svg>
              <span>DPIA Module</span>
            </button>

            <button type="button" class="nav-btn">
              <svg
                class="nav-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
              </svg>
              <span>Risk Register</span>
            </button>

            <button type="button" class="nav-btn">
              <svg
                class="nav-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <line x1="18" y1="20" x2="18" y2="10"></line>
                <line x1="12" y1="20" x2="12" y2="4"></line>
                <line x1="6" y1="20" x2="6" y2="14"></line>
              </svg>
              <span>Reports</span>
            </button>

            <!-- Active Administration Tab -->
            <button type="button" class="nav-btn active">
              <svg
                class="nav-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <circle cx="12" cy="12" r="3"></circle>
                <path
                  d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"
                ></path>
              </svg>
              <span>Administration</span>
            </button>
          </nav>
        </div>
      </aside>

      <!-- Main Workspace -->
      <main class="main-content">
        <!-- Page Title Header -->
        <header class="admin-header">
          <div class="header-left">
            <span class="admin-tag">SYSTEM GOVERNANCE</span>
            <h1 class="page-title">System Administration</h1>
            <p class="page-desc">
              Manage enterprise access controls, user roles, security audit logs, and global system
              configurations.
            </p>
          </div>
          <button type="button" class="btn-primary-add" @click="handleAddUser">
            <svg
              class="plus-icn"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.5"
            >
              <line x1="12" y1="5" x2="12" y2="19"></line>
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
            <span>Provision User</span>
          </button>
        </header>

        <!-- Sub-Tab Navigation Header -->
        <div class="subtabs-bar">
          <button
            type="button"
            class="subtab-btn"
            :class="{ active: activeTab === 'users' }"
            @click="activeTab = 'users'"
          >
            <svg
              class="subtab-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
            <span>User Management & RBAC</span>
          </button>

          <button
            type="button"
            class="subtab-btn"
            :class="{ active: activeTab === 'audit' }"
            @click="activeTab = 'audit'"
          >
            <svg
              class="subtab-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
            </svg>
            <span>Security Audit Logs</span>
          </button>

          <button
            type="button"
            class="subtab-btn"
            :class="{ active: activeTab === 'settings' }"
            @click="activeTab = 'settings'"
          >
            <svg
              class="subtab-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <circle cx="12" cy="12" r="3"></circle>
              <path
                d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"
              ></path>
            </svg>
            <span>System Settings</span>
          </button>
        </div>

        <!-- ============================================ -->
        <!-- TAB 1: USER MANAGEMENT & RBAC                -->
        <!-- ============================================ -->
        <div v-if="activeTab === 'users'" class="tab-panel">
          <!-- Filter Controls -->
          <div class="filter-controls-row">
            <div class="search-filter-box">
              <svg
                class="search-filter-icn"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
              <input
                v-model="userSearchQuery"
                type="text"
                placeholder="Filter users by name, email, department..."
                class="filter-input"
              />
            </div>

            <div class="role-filter-group">
              <label class="filter-lbl">Role:</label>
              <select v-model="selectedRoleFilter" class="role-select">
                <option value="ALL">All Roles</option>
                <option value="Global Controller">Global Controller</option>
                <option value="Data Protection Officer">Data Protection Officer</option>
                <option value="Senior Privacy Counsel">Senior Privacy Counsel</option>
                <option value="Project Manager">Project Manager</option>
                <option value="Security Auditor">Security Auditor</option>
              </select>
            </div>
          </div>

          <!-- User Data Table -->
          <div class="panel-box table-card">
            <table class="data-table">
              <thead>
                <tr>
                  <th>USER</th>
                  <th>ROLE</th>
                  <th>DEPARTMENT</th>
                  <th>AUTH SOURCE</th>
                  <th>STATUS</th>
                  <th>LAST LOGIN</th>
                  <th class="text-right">ACTIONS</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="u in filteredUsers" :key="u.id">
                  <td>
                    <div class="user-cell">
                      <img :src="u.avatar" :alt="u.name" class="table-avatar" />
                      <div class="user-meta">
                        <span class="u-name">{{ u.name }}</span>
                        <span class="u-email">{{ u.email }}</span>
                      </div>
                    </div>
                  </td>
                  <td>
                    <span class="role-badge" :class="u.role.toLowerCase().replace(/\s+/g, '-')">
                      {{ u.role }}
                    </span>
                  </td>
                  <td class="dept-text">{{ u.department }}</td>
                  <td>
                    <div class="auth-source-tag">
                      <svg class="microsoft-icon" viewBox="0 0 23 23">
                        <path fill="#f35325" d="M1 1h10v10H1z" />
                        <path fill="#81bc06" d="M12 1h10v10H12z" />
                        <path fill="#05a6f0" d="M1 12h10v10H1z" />
                        <path fill="#ffba08" d="M12 12h10v10H12z" />
                      </svg>
                      <span>{{ u.authSource }}</span>
                    </div>
                  </td>
                  <td>
                    <span class="status-pill" :class="u.status.toLowerCase()">
                      ● {{ u.status }}
                    </span>
                  </td>
                  <td class="time-text">{{ u.lastLogin }}</td>
                  <td class="text-right">
                    <button type="button" class="action-btn" title="Edit Permissions">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                        <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                      </svg>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- ============================================ -->
        <!-- TAB 2: SECURITY AUDIT LOGS                   -->
        <!-- ============================================ -->
        <div v-else-if="activeTab === 'audit'" class="tab-panel">
          <div class="panel-box table-card">
            <div class="table-header-bar">
              <h3 class="panel-title">Real-Time Security Event Stream</h3>
              <span class="live-stream-badge">● LIVE STREAMING</span>
            </div>

            <table class="data-table">
              <thead>
                <tr>
                  <th>TIMESTAMP</th>
                  <th>USER</th>
                  <th>ACTION PERFORMED</th>
                  <th>TARGET MODULE</th>
                  <th>IP ADDRESS</th>
                  <th>SEVERITY</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="log in auditLogs" :key="log.id">
                  <td class="time-code">{{ log.timestamp }}</td>
                  <td class="font-medium">{{ log.user }}</td>
                  <td class="action-text">{{ log.action }}</td>
                  <td>
                    <span class="module-tag">{{ log.module }}</span>
                  </td>
                  <td class="ip-code">{{ log.ipAddress }}</td>
                  <td>
                    <span class="severity-tag" :class="log.severity.toLowerCase()">
                      {{ log.severity }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- ============================================ -->
        <!-- TAB 3: SYSTEM SETTINGS                       -->
        <!-- ============================================ -->
        <div v-else-if="activeTab === 'settings'" class="tab-panel">
          <div class="panel-box settings-card">
            <form @submit.prevent="handleSaveSettings" class="settings-form">
              <div class="form-section">
                <h3 class="form-section-title">Microsoft Entra ID SSO Integration</h3>

                <div class="form-grid-2">
                  <div class="form-group">
                    <label class="form-label">ENTRA TENANT ID</label>
                    <input v-model="entraTenantId" type="text" class="form-input" />
                  </div>
                  <div class="form-group">
                    <label class="form-label">APPLICATION CLIENT ID</label>
                    <input v-model="entraClientId" type="text" class="form-input" />
                  </div>
                </div>
              </div>

              <div class="form-section">
                <h3 class="form-section-title">DPIA Risk Engine Rules</h3>

                <div class="form-group max-w-md">
                  <label class="form-label"
                    >DPIA MANDATORY RISK THRESHOLD (SCORE: {{ dpiaThreshold }})</label
                  >
                  <input
                    v-model.number="dpiaThreshold"
                    type="range"
                    min="30"
                    max="90"
                    class="range-slider"
                  />
                  <p class="field-caption">
                    Any assessment scoring at or above this score will trigger mandatory DPO review.
                  </p>
                </div>

                <div class="toggle-row">
                  <div>
                    <h4 class="toggle-title">Automated DPO Task Routing</h4>
                    <p class="toggle-desc">
                      Automatically route high-risk assessments to the primary DPO inbox upon
                      completion of screening.
                    </p>
                  </div>
                  <input v-model="autoDpoAssignment" type="checkbox" class="toggle-switch" />
                </div>
              </div>

              <div class="form-section">
                <h3 class="form-section-title">Data Retention & Compliance Governance</h3>

                <div class="form-group max-w-sm">
                  <label class="form-label">AUDIT LOG RETENTION PERIOD (DAYS)</label>
                  <select v-model="auditLogRetentionDays" class="form-select">
                    <option :value="90">90 Days</option>
                    <option :value="180">180 Days</option>
                    <option :value="365">365 Days (1 Year - GDPR Recommended)</option>
                    <option :value="730">730 Days (2 Years)</option>
                  </select>
                </div>
              </div>

              <div class="form-actions-footer">
                <button type="submit" class="btn-save-settings">Save Configurations</button>
              </div>
            </form>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
.admin-layout {
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

/* Left Sidebar Navigation */
.left-sidebar {
  width: 240px;
  background-color: #ffffff;
  border-right: 1px solid #e2e8f0;
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  gap: 28px;
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

/* Main Workspace */
.main-content {
  flex: 1;
  padding: 36px 48px;
  background-color: #f8fafc;
  overflow-y: auto;
}

.admin-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 24px;
}

.admin-tag {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #0d9488;
  display: block;
  margin-bottom: 4px;
}

.page-title {
  font-family: var(--font-family);
  font-size: 30px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.02em;
}

.page-desc {
  font-size: 14px;
  color: #64748b;
  margin-top: 4px;
  max-width: 600px;
}

.btn-primary-add {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 44px;
  padding: 0 20px;
  background: #030712;
  color: #ffffff;
  border: none;
  border-radius: 10px;
  font-family: var(--font-family);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(3, 7, 18, 0.15);
}

.plus-icn {
  width: 16px;
  height: 16px;
}

/* Subtabs Bar */
.subtabs-bar {
  display: flex;
  gap: 12px;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 28px;
  padding-bottom: 1px;
}

.subtab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 18px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  font-family: var(--font-family);
  font-size: 14px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.15s ease;
}

.subtab-btn:hover {
  color: #0f172a;
}

.subtab-btn.active {
  color: #0f2942;
  border-bottom-color: #0f2942;
}

.subtab-icon {
  width: 17px;
  height: 17px;
}

/* Filter Controls */
.filter-controls-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 20px;
}

.search-filter-box {
  position: relative;
  flex: 1;
  max-width: 420px;
  display: flex;
  align-items: center;
}

.search-filter-icn {
  position: absolute;
  left: 14px;
  width: 16px;
  height: 16px;
  color: #94a3b8;
}

.filter-input {
  width: 100%;
  height: 42px;
  padding: 0 16px 0 42px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-family: var(--font-family);
  font-size: 13.5px;
  outline: none;
}

.role-filter-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-lbl {
  font-size: 13px;
  font-weight: 600;
  color: #475569;
}

.role-select {
  height: 42px;
  padding: 0 16px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-family: var(--font-family);
  font-size: 13.5px;
  color: #0f172a;
  outline: none;
  cursor: pointer;
}

/* Table styling */
.panel-box {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
}

.table-card {
  padding: 0;
  overflow: hidden;
}

.table-header-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #f1f5f9;
}

.panel-title {
  font-family: var(--font-family);
  font-size: 17px;
  font-weight: 700;
  color: #0f172a;
}

.live-stream-badge {
  font-size: 11px;
  font-weight: 800;
  color: #10b981;
  background: #ecfdf5;
  padding: 4px 10px;
  border-radius: 6px;
  letter-spacing: 0.05em;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.data-table th {
  background: #f8fafc;
  padding: 14px 24px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #64748b;
  border-bottom: 1px solid #e2e8f0;
}

.data-table td {
  padding: 16px 24px;
  border-bottom: 1px solid #f1f5f9;
  font-size: 13.5px;
  color: #334155;
  vertical-align: middle;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.table-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
}

.user-meta {
  display: flex;
  flex-direction: column;
}

.u-name {
  font-weight: 700;
  color: #0f172a;
}

.u-email {
  font-size: 12px;
  color: #64748b;
}

.role-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 11.5px;
  font-weight: 700;
  background: #f1f5f9;
  color: #334155;
}

.role-badge.global-controller {
  background: #e0f2fe;
  color: #0369a1;
}

.role-badge.data-protection-officer {
  background: #ccfbf1;
  color: #0f766e;
}

.auth-source-tag {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #475569;
}

.microsoft-icon {
  width: 14px;
  height: 14px;
}

.status-pill {
  font-size: 12px;
  font-weight: 700;
}

.status-pill.active {
  color: #10b981;
}

.status-pill.pending {
  color: #f59e0b;
}

.time-text {
  font-size: 12.5px;
  color: #64748b;
}

.time-code {
  font-family: monospace;
  font-size: 12px;
  color: #64748b;
}

.ip-code {
  font-family: monospace;
  font-size: 12px;
  color: #0f172a;
}

.module-tag {
  background: #f1f5f9;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 11.5px;
  font-weight: 600;
}

.severity-tag {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.05em;
}

.severity-tag.warning {
  background: #fef3c7;
  color: #b45309;
}

.severity-tag.info {
  background: #e0f2fe;
  color: #0369a1;
}

.severity-tag.critical {
  background: #fef2f2;
  color: #dc2626;
}

.action-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #64748b;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background: #f1f5f9;
  color: #0f172a;
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.text-right {
  text-align: right;
}

/* Settings Form */
.settings-card {
  max-width: 800px;
  padding: 32px;
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.form-section-title {
  font-family: var(--font-family);
  font-size: 16px;
  font-weight: 700;
  color: #0f172a;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 8px;
}

.form-grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.max-w-md {
  max-width: 480px;
}

.form-label {
  font-size: 11.5px;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #475569;
}

.form-input,
.form-select {
  height: 44px;
  padding: 0 16px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  font-family: var(--font-family);
  font-size: 14px;
  color: #0f172a;
  outline: none;
}

.range-slider {
  width: 100%;
  accent-color: #0f2942;
  margin-top: 6px;
}

.toggle-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f8fafc;
  padding: 16px;
  border-radius: 10px;
}

.toggle-title {
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
}

.toggle-desc {
  font-size: 12.5px;
  color: #64748b;
  margin-top: 2px;
}

.toggle-switch {
  width: 20px;
  height: 20px;
  accent-color: #0f2942;
  cursor: pointer;
}

.form-actions-footer {
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.btn-save-settings {
  height: 44px;
  padding: 0 24px;
  background: #030712;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  font-family: var(--font-family);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(3, 7, 18, 0.15);
}

@media (max-width: 1024px) {
  .left-sidebar {
    display: none;
  }
}
</style>
