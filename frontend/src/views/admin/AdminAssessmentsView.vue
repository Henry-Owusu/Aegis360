<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AdminLayout from './components/AdminLayout.vue'
import { dpiaApi, type AssessmentSummary } from '@/services/api'

// ─── State ────────────────────────────────────────────────────────────────────

const assessments = ref<AssessmentSummary[]>([])
const isLoading = ref(true)
const searchQuery = ref('')
const filterStatus = ref('all')

// ─── Computed ─────────────────────────────────────────────────────────────────

const filteredAssessments = computed(() => {
  return assessments.value.filter((a) => {
    const matchesSearch =
      !searchQuery.value ||
      a.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      a.project_manager.toLowerCase().includes(searchQuery.value.toLowerCase())

    const matchesStatus = filterStatus.value === 'all' || a.status === filterStatus.value

    return matchesSearch && matchesStatus
  })
})

const totalAssessments = computed(() => assessments.value.length)
const totalPending = computed(
  () =>
    assessments.value.filter(
      (a) => a.status !== 'approved' && a.status !== 'rejected' && a.status !== 'draft',
    ).length,
)

// ─── Actions ──────────────────────────────────────────────────────────────────

const fetchData = async () => {
  isLoading.value = true
  try {
    const res = await dpiaApi.listAssessments()
    assessments.value = res.assessments
  } catch (err) {
    console.error('Failed to load assessments:', err)
  } finally {
    isLoading.value = false
  }
}

const formatDate = (iso: string) =>
  new Date(iso).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })

const getStatusClass = (status: string) => {
  switch (status.toLowerCase()) {
    case 'approved':
      return 'status-approved'
    case 'rejected':
      return 'status-rejected'
    case 'draft':
      return 'status-draft'
    default:
      return 'status-pending'
  }
}

const getStatusLabel = (status: string) => {
  return status.charAt(0).toUpperCase() + status.slice(1).replace('_', ' ')
}

onMounted(fetchData)
</script>

<template>
  <AdminLayout>
    <!-- Page Header -->
    <div class="page-header">
      <div>
        <h2 class="page-title">Assessments</h2>
        <p class="page-sub">Monitor and manage all DPIA assessments across the organization</p>
      </div>
      <div class="header-stats">
        <div class="stat-chip blue">
          <span class="dot"></span>
          {{ totalAssessments }} Total
        </div>
        <div class="stat-chip orange">
          <span class="dot"></span>
          {{ totalPending }} In Progress
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
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by title or project manager..."
        />
      </div>
      <div class="filters">
        <select v-model="filterStatus" class="filter-select">
          <option value="all">All Statuses</option>
          <option value="draft">Draft</option>
          <option value="screening">Screening</option>
          <option value="dpo_review">DPO Review</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state">
      <div class="spinner-ring"></div>
      <p>Loading assessments...</p>
    </div>

    <!-- Assessments Table -->
    <div v-else class="table-card">
      <table class="data-table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Project Manager</th>
            <th>Department</th>
            <th>Status</th>
            <th>Created</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredAssessments.length === 0">
            <td colspan="5" class="empty-row">No assessments match your filters</td>
          </tr>
          <tr v-for="assessment in filteredAssessments" :key="assessment.id">
            <!-- Title -->
            <td class="primary-cell">
              <span class="item-title">{{ assessment.title }}</span>
              <span class="item-sub">ID: {{ assessment.id.substring(0, 8) }}</span>
            </td>

            <!-- PM -->
            <td>
              <div class="pm-info">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                  <circle cx="12" cy="7" r="4"></circle>
                </svg>
                {{ assessment.project_manager }}
              </div>
            </td>

            <!-- Dept -->
            <td class="dept-cell">{{ assessment.department_function_agency || 'Unspecified' }}</td>

            <!-- Status -->
            <td>
              <span class="status-badge" :class="getStatusClass(assessment.status)">
                <span class="status-dot"></span>
                {{ getStatusLabel(assessment.status) }}
              </span>
            </td>

            <!-- Date -->
            <td class="date-cell">{{ formatDate(assessment.created_at) }}</td>
          </tr>
        </tbody>
      </table>
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
.stat-chip.blue {
  background: rgba(59, 130, 246, 0.12);
  color: #60a5fa;
}
.stat-chip.orange {
  background: rgba(245, 132, 37, 0.12);
  color: #fdba74;
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
.data-table {
  width: 100%;
  border-collapse: collapse;
}
.data-table th {
  text-align: left;
  padding: 18px 20px;
  color: #92929d;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}
.data-table td {
  padding: 16px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.03);
  vertical-align: middle;
}
.data-table tr:last-child td {
  border-bottom: none;
}
.data-table tr:hover td {
  background: rgba(255, 255, 255, 0.02);
}
.empty-row {
  text-align: center;
  color: #92929d;
  font-size: 14px;
  padding: 48px !important;
}

/* ── Cells ───────────────────────────────────────────────────── */
.primary-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.item-title {
  font-size: 14px;
  font-weight: 600;
  color: #ffffff;
}
.item-sub {
  font-size: 12px;
  color: #92929d;
  font-family: monospace;
}

.pm-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #e2e8f0;
  font-size: 13px;
}
.pm-info svg {
  width: 14px;
  height: 14px;
  color: #92929d;
}

.dept-cell {
  color: #94a3b8;
  font-size: 13px;
}
.date-cell {
  color: #92929d;
  font-size: 13px;
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
.status-approved {
  background: rgba(34, 197, 94, 0.12);
  color: #4ade80;
}
.status-rejected {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
}
.status-draft {
  background: rgba(148, 163, 184, 0.1);
  color: #94a3b8;
}
.status-pending {
  background: rgba(245, 132, 37, 0.12);
  color: #fdba74;
}
.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}
</style>
