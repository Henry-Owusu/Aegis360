import { createRouter, createWebHistory } from 'vue-router'
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

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/modules',
      name: 'modules',
      component: ModulesView
    },
    {
      path: '/pm/dashboard',
      name: 'pm-dashboard',
      component: DpiaDashboardView
    },
    {
      path: '/pm/dpias',
      name: 'pm-dpias',
      component: PmDpiaListView
    },
    {
      path: '/pm/dpia/new',
      name: 'pm-dpia-new',
      component: DpiaAssessmentView
    },
    {
      path: '/pm/risk-register',
      name: 'pm-risk-register',
      component: PmRiskRegisterView
    },
    {
      path: '/pm/reports',
      name: 'pm-reports',
      component: PmReportsView
    },
    {
      path: '/dpo/dashboard',
      name: 'dpo-dashboard',
      component: DpoDashboardView
    },
    {
      path: '/dpo/dpias',
      name: 'dpo-dpias',
      component: DpoDpiaListView
    },
    {
      path: '/dpo/risk-register',
      name: 'dpo-risk-register',
      component: DpoRiskRegisterView
    },
    {
      path: '/dpo/reports',
      name: 'dpo-reports',
      component: DpoReportsView
    },
    {
      path: '/dpo/questions',
      name: 'dpo-questions',
      component: DpoQuestionManagementView
    },
    {
      path: '/admin',
      redirect: '/admin/dashboard'
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: AdminDashboardView
    },
    {
      path: '/admin/users',
      name: 'admin-users',
      component: AdminUsersView
    },
    {
      path: '/admin/assessments',
      name: 'admin-assessments',
      component: AdminAssessmentsView
    },
    {
      path: '/admin/modules',
      name: 'admin-modules',
      component: AdminModulesView
    },
    {
      path: '/admin/questions',
      name: 'admin-questions',
      component: AdminQuestionsView
    },
    {
      path: '/admin/roles',
      name: 'admin-roles',
      component: AdminRolesView
    },
    {
      path: '/admin/permissions',
      name: 'admin-permissions',
      component: AdminPermissionsView
    },
    {
      path: '/admin/settings',
      name: 'admin-settings',
      component: AdminSettingsView
    }
  ]
})

export default router
