<script setup lang="ts">
import { ref } from 'vue'
import AdminLayout from './components/AdminLayout.vue'

// ─── Mock Data ────────────────────────────────────────────────────────────────

const modules = ref([
  {
    id: 'm1',
    name: 'DPIA Automation',
    description: 'Core module for Data Protection Impact Assessments',
    enabled: true,
    core: true,
  },
  {
    id: 'm2',
    name: 'Risk Register',
    description: 'Centralized repository for identifying and mitigating privacy risks',
    enabled: true,
    core: false,
  },
  {
    id: 'm3',
    name: 'Data Subject Requests (DSR)',
    description: 'Manage and automate responses to user privacy requests',
    enabled: false,
    core: false,
  },
  {
    id: 'm4',
    name: 'Vendor Risk Management',
    description: 'Assess and monitor third-party vendors for compliance',
    enabled: false,
    core: false,
  },
  {
    id: 'm5',
    name: 'Audit & Compliance',
    description: 'Track system usage and compliance with regulatory frameworks',
    enabled: true,
    core: false,
  },
])

const toggleModule = (mod: any) => {
  if (mod.core) return // Core modules cannot be disabled
  mod.enabled = !mod.enabled
}
</script>

<template>
  <AdminLayout>
    <div class="page-header">
      <div>
        <h2 class="page-title">Modules Configuration</h2>
        <p class="page-sub">Enable or disable Aegis360 system modules for your organization</p>
      </div>
    </div>

    <!-- Modules Grid -->
    <div class="modules-grid">
      <div
        v-for="mod in modules"
        :key="mod.id"
        class="module-card"
        :class="{ 'is-disabled': !mod.enabled }"
      >
        <div class="card-header">
          <div class="title-group">
            <h3 class="module-name">{{ mod.name }}</h3>
            <span v-if="mod.core" class="badge-core">Core</span>
          </div>

          <!-- Toggle Switch -->
          <button
            class="toggle-switch"
            :class="{ active: mod.enabled, locked: mod.core }"
            @click="toggleModule(mod)"
          >
            <div class="knob"></div>
          </button>
        </div>

        <p class="module-desc">{{ mod.description }}</p>

        <div class="card-footer">
          <button v-if="mod.enabled" class="config-btn">Configure Module</button>
          <button v-else class="config-btn disabled" disabled>Requires Activation</button>
        </div>
      </div>
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

/* ── Modules Grid ────────────────────────────────────────────── */
.modules-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 24px;
}
.module-card {
  background: #1c1c24;
  border-radius: 20px;
  padding: 24px;
  border: 1px solid rgba(255, 255, 255, 0.04);
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}
.module-card.is-disabled {
  opacity: 0.6;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}
.title-group {
  display: flex;
  align-items: center;
  gap: 10px;
}
.module-name {
  font-size: 18px;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
}
.badge-core {
  background: rgba(239, 68, 68, 0.1);
  color: #f87171;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.module-desc {
  color: #92929d;
  font-size: 14px;
  line-height: 1.5;
  margin: 0 0 24px;
  flex: 1;
}

/* ── Toggle Switch ───────────────────────────────────────────── */
.toggle-switch {
  width: 44px;
  height: 24px;
  border-radius: 12px;
  background: #2c2c35;
  border: none;
  position: relative;
  cursor: pointer;
  transition: background 0.3s;
}
.toggle-switch.active {
  background: #f58425;
}
.toggle-switch.locked {
  cursor: not-allowed;
  opacity: 0.8;
}
.knob {
  width: 20px;
  height: 20px;
  background: #ffffff;
  border-radius: 50%;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: transform 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
.toggle-switch.active .knob {
  transform: translateX(20px);
}

/* ── Footer ──────────────────────────────────────────────────── */
.card-footer {
  display: flex;
}
.config-btn {
  flex: 1;
  background: rgba(255, 255, 255, 0.05);
  color: #e2e8f0;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 12px 0;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.config-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}
.config-btn.disabled {
  background: transparent;
  border-color: rgba(255, 255, 255, 0.05);
  color: #64748b;
  cursor: not-allowed;
}
</style>
