import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, saveToken, clearToken, getToken } from '@/services/api'

export interface UserProfile {
  id: string
  name: string
  firstName: string
  lastName: string
  email: string
  roles: string[]
  permissions: string[]
  avatar: string
}

// Default avatar per role
const ROLE_AVATARS: Record<string, string> = {
  DPO: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
  PM: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80',
  'System Administrator':
    'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80',
  Approver:
    'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80',
}

const DEFAULT_AVATAR =
  'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80'

const EMPTY_USER: UserProfile = {
  id: '',
  name: '',
  firstName: '',
  lastName: '',
  email: '',
  roles: [],
  permissions: [],
  avatar: DEFAULT_AVATAR,
}

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)
  const isLoading = ref(false)
  const user = ref<UserProfile>({ ...EMPTY_USER })

  // ─── Computed helpers ─────────────────────────────────────────────────────

  /** Primary role is the first role returned by the backend */
  const primaryRole = computed(() => user.value.roles[0] ?? '')

  const hasRole = (role: string) => user.value.roles.includes(role)
  const hasPermission = (permission: string) => user.value.permissions.includes(permission)

  // ─── Session Hydration ────────────────────────────────────────────────────

  /**
   * On app startup, check if a JWT is stored in localStorage.
   * If so, reconstruct the user session from the token payload
   * (we store the user metadata alongside the token).
   */
  const hydrateFromStorage = () => {
    const token = getToken()
    const storedUser = localStorage.getItem('aegis_user')

    if (token && storedUser) {
      try {
        const parsed = JSON.parse(storedUser) as UserProfile
        user.value = parsed
        isAuthenticated.value = true
      } catch {
        // Corrupt storage — clear it
        clearToken()
        localStorage.removeItem('aegis_user')
      }
    }
  }

  // ─── Actions ──────────────────────────────────────────────────────────────

  /**
   * Authenticate against the real Flask backend.
   * Returns the primary role string so the caller can redirect appropriately.
   */
  const login = async (email: string): Promise<string> => {
    isLoading.value = true
    try {
      const response = await authApi.mockLogin(email)

      // Persist the JWT
      saveToken(response.access_token)

      // Derive display name and avatar
      const primaryRoleName = response.roles[0] ?? 'User'
      const avatar = ROLE_AVATARS[primaryRoleName] ?? DEFAULT_AVATAR
      const fullName = `${response.user.first_name} ${response.user.last_name}`

      const profile: UserProfile = {
        id: response.user.id,
        name: fullName,
        firstName: response.user.first_name,
        lastName: response.user.last_name,
        email: response.user.email,
        roles: response.roles,
        permissions: response.permissions,
        avatar,
      }

      user.value = profile
      isAuthenticated.value = true

      // Persist user metadata for page-refresh hydration
      localStorage.setItem('aegis_user', JSON.stringify(profile))

      return primaryRoleName
    } finally {
      isLoading.value = false
    }
  }

  const logout = () => {
    clearToken()
    localStorage.removeItem('aegis_user')
    isAuthenticated.value = false
    user.value = { ...EMPTY_USER }
  }

  return {
    isAuthenticated,
    isLoading,
    user,
    primaryRole,
    hasRole,
    hasPermission,
    login,
    logout,
    hydrateFromStorage,
  }
})
