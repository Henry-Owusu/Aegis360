import { defineStore } from 'pinia'
import { ref } from 'vue'
import { dpiaApi, type AssessmentSummary } from '@/services/api'

export const useAssessmentStore = defineStore('assessments', () => {
  const assessments = ref<AssessmentSummary[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const total = ref(0)

  /**
   * Fetch all assessments from the backend, with an optional status filter.
   * e.g. fetchAssessments('draft,screening')
   */
  const fetchAssessments = async (status?: string) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await dpiaApi.listAssessments(status)
      assessments.value = response.assessments
      total.value = response.total
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Failed to load assessments'
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Create a new DPIA assessment
   */
  const createAssessment = async (payload: Parameters<typeof dpiaApi.createAssessment>[0]) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await dpiaApi.createAssessment(payload)
      // Prepend the new assessment to the local list
      assessments.value = [response.assessment, ...assessments.value]
      total.value += 1
      return response.assessment
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Failed to create assessment'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Return counts by status — useful for dashboard KPI cards
   */
  const countByStatus = (status: string) =>
    assessments.value.filter((a) => a.status === status).length

  return {
    assessments,
    isLoading,
    error,
    total,
    fetchAssessments,
    createAssessment,
    countByStatus,
  }
})
