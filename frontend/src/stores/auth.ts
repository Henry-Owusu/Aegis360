import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface UserProfile {
  name: string
  role: string
  avatar: string
  email: string
}

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)
  const user = ref<UserProfile>({
    name: 'Guest User',
    role: 'Guest',
    email: '',
    avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80'
  })

  // Mock roles mapped by email for easy testing
  const MOCK_USERS: Record<string, Partial<UserProfile>> = {
    'admin@aegis360.com': {
      name: 'Executive Admin',
      role: 'System Admin',
      avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80'
    },
    'pm@aegis360.com': {
      name: 'Project Manager',
      role: 'Project Manager',
      avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80'
    },
    'dpo@aegis360.com': {
      name: 'Data Protection Officer',
      role: 'DPO',
      avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80'
    },
    'approver@aegis360.com': {
      name: 'System Approver',
      role: 'Approver',
      avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80'
    }
  }

  const login = (email: string) => {
    const foundUser = MOCK_USERS[email.toLowerCase()]
    if (foundUser) {
      user.value = {
        ...user.value,
        ...foundUser,
        email: email
      }
      isAuthenticated.value = true
      return true
    }
    return false
  }

  const logout = () => {
    isAuthenticated.value = false
    user.value = {
      name: 'Guest User',
      role: 'Guest',
      email: '',
      avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80'
    }
  }

  return {
    isAuthenticated,
    user,
    login,
    logout
  }
})
