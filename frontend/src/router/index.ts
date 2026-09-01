import { createRouter, createWebHistory } from 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    public?: boolean
    requiresAuth?: boolean
    requiresRole?: string
  }
}

import { useAuthStore } from '@/stores/auth'
import LoginView from '@/views/auth/LoginView.vue'
import ModulesView from '@/views/dashboard/ModulesView.vue'
import DpiaDashboardView from '@/views/dpia/DpiaDashboardView.vue'
import DpiaAssessmentView from '@/views/dpia/DpiaAssessmentView.vue'
import PmDpiaListView from '@/views/dpia/PmDpiaListView.vue'
import PmRiskRegisterView from '@/views/dpia/PmRiskRegisterView.vue'
import PmReportsView from '@/views/dpia/PmReportsView.vue'
import AdminDashboardView from '@/views/admin/AdminDashboardView.vue'
import DpoDashboardView from '@/views/dpo/DpoDashboardView.vue'
import DpoQuestionManagementView from '@/views/dpo/DpoQuestionManagementView.vue'
import DpoDpiaListView from '@/views/dpo/DpoDpiaListView.vue'
import DpoRiskRegisterView from '@/views/dpo/DpoRiskRegisterView.vue'
import DpoReportsView from '@/views/dpo/DpoReportsView.vue'
import AdminUsersView from '@/views/admin/AdminUsersView.vue'
import AdminAssessmentsView from '@/views/admin/AdminAssessmentsView.vue'
import AdminModulesView from '@/views/admin/AdminModulesView.vue'
import AdminQuestionsView from '@/views/admin/AdminQuestionsView.vue'
import AdminRolesView from '@/views/admin/AdminRolesView.vue'
import AdminPermissionsView from '@/views/admin/AdminPermissionsView.vue'
import AdminSettingsView from '@/views/admin/AdminSettingsView.vue'
import AdminHelpCenterView from '@/views/admin/AdminHelpCenterView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: '/login',
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { public: true },
    },
    {
      path: '/modules',
      name: 'modules',
      component: ModulesView,
      meta: { requiresAuth: true },
    },
    // ── Project Manager ─────────────────────────────────────────
    {
      path: '/pm/dashboard',
      name: 'pm-dashboard',
      component: DpiaDashboardView,
      meta: { requiresAuth: true, requiresRole: 'PM' },
    },
    {
      path: '/pm/dpias',
      name: 'pm-dpias',
      component: PmDpiaListView,
      meta: { requiresAuth: true, requiresRole: 'PM' },
    },
    {
      path: '/pm/dpia/new',
      name: 'pm-dpia-new',
      component: DpiaAssessmentView,
      meta: { requiresAuth: true, requiresRole: 'PM' },
    },
    {
      path: '/pm/risk-register',
      name: 'pm-risk-register',
      component: PmRiskRegisterView,
      meta: { requiresAuth: true, requiresRole: 'PM' },
    },
    {
      path: '/pm/reports',
      name: 'pm-reports',
      component: PmReportsView,
      meta: { requiresAuth: true, requiresRole: 'PM' },
    },
    // ── DPO ─────────────────────────────────────────────────────
    {
      path: '/dpo/dashboard',
      name: 'dpo-dashboard',
      component: DpoDashboardView,
      meta: { requiresAuth: true, requiresRole: 'DPO' },
    },
    {
      path: '/dpo/dpias',
      name: 'dpo-dpias',
      component: DpoDpiaListView,
      meta: { requiresAuth: true, requiresRole: 'DPO' },
    },
    {
      path: '/dpo/risk-register',
      name: 'dpo-risk-register',
      component: DpoRiskRegisterView,
      meta: { requiresAuth: true, requiresRole: 'DPO' },
    },
    {
      path: '/dpo/reports',
      name: 'dpo-reports',
      component: DpoReportsView,
      meta: { requiresAuth: true, requiresRole: 'DPO' },
    },
    {
      path: '/dpo/questions',
      name: 'dpo-questions',
      component: DpoQuestionManagementView,
      meta: { requiresAuth: true, requiresRole: 'DPO' },
    },
    // ── System Admin ─────────────────────────────────────────────
    {
      path: '/admin',
      redirect: '/admin/dashboard',
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: AdminDashboardView,
      meta: { requiresAuth: true, requiresRole: 'System Administrator' },
    },
    {
      path: '/admin/users',
      name: 'admin-users',
      component: AdminUsersView,
      meta: { requiresAuth: true, requiresRole: 'System Administrator' },
    },
    {
      path: '/admin/assessments',
      name: 'admin-assessments',
      component: AdminAssessmentsView,
      meta: { requiresAuth: true, requiresRole: 'System Administrator' },
    },
    {
      path: '/admin/modules',
      name: 'admin-modules',
      component: AdminModulesView,
      meta: { requiresAuth: true, requiresRole: 'System Administrator' },
    },
    {
      path: '/admin/questions',
      name: 'admin-questions',
      component: AdminQuestionsView,
      meta: { requiresAuth: true, requiresRole: 'System Administrator' },
    },
    {
      path: '/admin/roles',
      name: 'admin-roles',
      component: AdminRolesView,
      meta: { requiresAuth: true, requiresRole: 'System Administrator' },
    },
    {
      path: '/admin/permissions',
      name: 'admin-permissions',
      component: AdminPermissionsView,
      meta: { requiresAuth: true, requiresRole: 'System Administrator' },
    },
    {
      path: '/admin/settings',
      name: 'admin-settings',
      component: AdminSettingsView,
      meta: { requiresAuth: true, requiresRole: 'System Administrator' },
    },
    {
      path: '/admin/help',
      name: 'admin-help',
      component: AdminHelpCenterView,
      meta: { requiresAuth: true, requiresRole: 'System Administrator' },
    },
  ],
})

// ─── Global Navigation Guard ───────────────────────────────────────────────────
router.beforeEach((to) => {
  const authStore = useAuthStore()

  // Allow public routes (login page) through always
  if (to.meta.public) return true

  // All other routes require authentication
  if (!authStore.isAuthenticated) {
    return { name: 'login' }
  }

  // If a route requires a specific role, enforce it
  const requiredRole = to.meta.requiresRole as string | undefined
  if (requiredRole && !authStore.hasRole(requiredRole)) {
    // Redirect to their own dashboard instead of a blank/error page
    const fallback =
      authStore.primaryRole === 'System Administrator'
        ? '/admin/dashboard'
        : authStore.primaryRole === 'DPO'
          ? '/dpo/dashboard'
          : authStore.primaryRole === 'PM'
            ? '/pm/dashboard'
            : '/modules'
    return fallback
  }

  return true
})

export default router
