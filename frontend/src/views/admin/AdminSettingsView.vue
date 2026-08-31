<script setup lang="ts">
import { ref } from 'vue'
import AdminLayout from './components/AdminLayout.vue'

const activeTab = ref('general')

const tabs = [
  { id: 'general', name: 'General Settings', icon: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z' },
  { id: 'security', name: 'Security & Auth', icon: 'M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z' },
  { id: 'notifications', name: 'Notifications', icon: 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9' },
  { id: 'branding', name: 'Theme & Branding', icon: 'M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01' }
]
</script>

<template>
  <AdminLayout>
    <div class="page-header">
      <div>
        <h2 class="page-title">System Settings</h2>
        <p class="page-sub">Configure global application behavior and preferences</p>
      </div>
    </div>

    <div class="settings-container">
      <!-- Sidebar Tabs -->
      <div class="settings-sidebar">
        <button 
          v-for="tab in tabs" :key="tab.id"
          class="tab-btn" 
          :class="{ active: activeTab === tab.id }"
          @click="activeTab = tab.id"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path :d="tab.icon"></path>
            <!-- Special case for center circle in settings icon -->
            <circle v-if="tab.id === 'general'" cx="12" cy="12" r="3"></circle>
          </svg>
          {{ tab.name }}
        </button>
      </div>

      <!-- Content Area -->
      <div class="settings-content">
        
        <!-- General Settings -->
        <div v-if="activeTab === 'general'" class="settings-panel">
          <h3>General Settings</h3>
          <p class="panel-desc">Manage basic application details.</p>
          
          <div class="form-group">
            <label>Organization Name</label>
            <input type="text" value="Aegis360 Compliance" class="form-input" />
          </div>
          
          <div class="form-group">
            <label>Support Email Address</label>
            <input type="email" value="support@aegis360.com" class="form-input" />
          </div>
          
          <div class="form-group">
            <label>Timezone</label>
            <select class="form-input">
              <option>UTC (Coordinated Universal Time)</option>
              <option>EST (Eastern Standard Time)</option>
              <option>PST (Pacific Standard Time)</option>
              <option>GMT (Greenwich Mean Time)</option>
            </select>
          </div>
          
          <button class="btn-save">Save Changes</button>
        </div>

        <!-- Security & Auth -->
        <div v-if="activeTab === 'security'" class="settings-panel">
          <h3>Security & Authentication</h3>
          <p class="panel-desc">Configure security policies and access controls.</p>
          
          <div class="setting-toggle-row">
            <div>
              <h4>Two-Factor Authentication (2FA)</h4>
              <p>Require all users to use 2FA for login</p>
            </div>
            <button class="toggle-switch active"><div class="knob"></div></button>
          </div>
          
          <div class="setting-toggle-row">
            <div>
              <h4>Single Sign-On (SSO)</h4>
              <p>Allow login via enterprise identity providers (SAML/OIDC)</p>
            </div>
            <button class="toggle-switch"><div class="knob"></div></button>
          </div>
          
          <div class="form-group" style="margin-top: 24px;">
            <label>Session Timeout (minutes)</label>
            <input type="number" value="60" class="form-input" />
          </div>
          
          <button class="btn-save">Save Changes</button>
        </div>

        <!-- Placeholder for others -->
        <div v-if="activeTab === 'notifications' || activeTab === 'branding'" class="settings-panel">
          <h3>{{ tabs.find(t => t.id === activeTab)?.name }}</h3>
          <p class="panel-desc">This section is currently under construction.</p>
          <div class="empty-state">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
            <h4>Coming Soon</h4>
            <p>We are actively working on building out this feature.</p>
          </div>
        </div>
        
      </div>
    </div>
  </AdminLayout>
</template>

<style scoped>
/* ── Page Header ─────────────────────────────────────────────── */
.page-header {
  margin-bottom: 32px;
}
.page-title {
  font-size: 24px; font-weight: 700; color: #FFFFFF; margin: 0 0 6px;
}
.page-sub {
  color: #92929D; font-size: 14px; margin: 0;
}

/* ── Settings Layout ─────────────────────────────────────────── */
.settings-container {
  display: flex;
  gap: 32px;
  background: #1C1C24;
  border-radius: 20px;
  border: 1px solid rgba(255,255,255,0.04);
  padding: 8px;
  min-height: 600px;
}
.settings-sidebar {
  width: 260px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 16px;
  border-right: 1px solid rgba(255,255,255,0.04);
}
.tab-btn {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 16px; border-radius: 12px;
  background: transparent; border: none;
  color: #92929D; font-size: 14px; font-weight: 600;
  text-align: left; cursor: pointer;
  transition: all 0.2s;
}
.tab-btn:hover {
  background: rgba(255,255,255,0.03); color: #E2E8F0;
}
.tab-btn.active {
  background: rgba(245,132,37,0.12); color: #FDBA74;
}
.tab-btn svg { width: 18px; height: 18px; }

/* ── Content Area ────────────────────────────────────────────── */
.settings-content {
  flex: 1;
  padding: 32px 48px 48px 16px;
}
.settings-panel h3 {
  font-size: 20px; font-weight: 700; color: #FFFFFF; margin: 0 0 8px;
}
.panel-desc {
  color: #92929D; font-size: 14px; margin: 0 0 32px;
}

/* ── Forms ───────────────────────────────────────────────────── */
.form-group {
  margin-bottom: 24px;
  max-width: 500px;
}
.form-group label {
  display: block; font-size: 13px; font-weight: 600;
  color: #E2E8F0; margin-bottom: 8px;
}
.form-input {
  width: 100%;
  background: #2C2C35;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  padding: 14px 16px;
  color: #FFFFFF;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}
.form-input:focus { border-color: #F58425; }

.setting-toggle-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 16px 0; border-bottom: 1px solid rgba(255,255,255,0.04);
  max-width: 600px;
}
.setting-toggle-row h4 { font-size: 15px; color: #FFFFFF; margin: 0 0 4px; }
.setting-toggle-row p { font-size: 13px; color: #92929D; margin: 0; }

.btn-save {
  margin-top: 24px;
  padding: 12px 24px; border-radius: 12px;
  background: linear-gradient(135deg, #FDBA74, #F58425);
  border: none; color: #FFFFFF;
  font-size: 14px; font-weight: 600; cursor: pointer;
}

/* ── Toggles ─────────────────────────────────────────────────── */
.toggle-switch {
  width: 44px; height: 24px; border-radius: 12px;
  background: #2C2C35; border: none; position: relative;
  cursor: pointer; transition: background 0.3s;
}
.toggle-switch.active { background: #F58425; }
.knob {
  width: 20px; height: 20px; background: #FFFFFF; border-radius: 50%;
  position: absolute; top: 2px; left: 2px;
  transition: transform 0.3s; box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.toggle-switch.active .knob { transform: translateX(20px); }

/* ── Empty State ─────────────────────────────────────────────── */
.empty-state {
  margin-top: 48px;
  display: flex; flex-direction: column; align-items: center; gap: 16px;
  color: #92929D; padding: 64px 0;
  background: rgba(255,255,255,0.01); border-radius: 16px;
  border: 1px dashed rgba(255,255,255,0.1);
}
.empty-state svg { width: 48px; height: 48px; color: #4A4A5A; }
.empty-state h4 { font-size: 18px; color: #FFFFFF; margin: 0; }
.empty-state p { margin: 0; }
</style>
