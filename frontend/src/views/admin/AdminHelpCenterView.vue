<script setup lang="ts">
import { ref } from 'vue'
import AdminLayout from './components/AdminLayout.vue'

const searchQuery = ref('')
const activeCategory = ref('getting-started')

const categories = [
  { id: 'getting-started', name: 'Getting Started', icon: 'M13 10V3L4 14h7v7l9-11h-7z' },
  { id: 'assessments', name: 'Assessments', icon: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z' },
  { id: 'users', name: 'User Management', icon: 'M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2' },
  { id: 'security', name: 'Security', icon: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z' }
]

const articles = ref([
  { id: 1, title: 'How to create a new user role?', category: 'users', excerpt: 'Learn how to define custom roles and assign specific permissions to them.' },
  { id: 2, title: 'Configuring DPIA automation triggers', category: 'assessments', excerpt: 'Set up automatic triggers for Data Protection Impact Assessments based on project scope.' },
  { id: 3, title: 'Setting up Two-Factor Authentication (2FA)', category: 'security', excerpt: 'A step-by-step guide to enabling mandatory 2FA for all administrative accounts.' },
  { id: 4, title: 'Introduction to Aegis360 Admin Suite', category: 'getting-started', excerpt: 'Welcome to your compliance command center. Learn how to navigate the main dashboard.' }
])
</script>

<template>
  <AdminLayout>
    <div class="help-center-hero">
      <h2>How can we help you today?</h2>
      <div class="search-box">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input v-model="searchQuery" type="text" placeholder="Search knowledge base articles, FAQs, and guides..." />
      </div>
    </div>

    <div class="help-content">
      <div class="categories-sidebar">
        <button 
          v-for="cat in categories" :key="cat.id"
          class="cat-btn"
          :class="{ active: activeCategory === cat.id }"
          @click="activeCategory = cat.id"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path :d="cat.icon"></path></svg>
          {{ cat.name }}
        </button>
      </div>

      <div class="articles-grid">
        <div v-for="art in articles.filter(a => a.category === activeCategory)" :key="art.id" class="article-card">
          <h4>{{ art.title }}</h4>
          <p>{{ art.excerpt }}</p>
          <button class="read-more">Read Article &rarr;</button>
        </div>
        
        <div v-if="articles.filter(a => a.category === activeCategory).length === 0" class="empty-state">
          No articles found for this category yet.
        </div>
      </div>
    </div>
    
    <div class="support-banner">
      <div class="support-text">
        <h3>Still need help?</h3>
        <p>Our dedicated compliance support team is available 24/7 to assist you.</p>
      </div>
      <button class="btn-support">Contact Support</button>
    </div>
  </AdminLayout>
</template>

<style scoped>
/* ── Hero ────────────────────────────────────────────────────── */
.help-center-hero {
  background: linear-gradient(135deg, rgba(245,132,37,0.1), rgba(28,28,36,0));
  border: 1px solid rgba(245,132,37,0.15);
  border-radius: 20px;
  padding: 64px 32px;
  text-align: center;
  margin-bottom: 32px;
}
.help-center-hero h2 {
  font-size: 32px; font-weight: 700; color: #FFFFFF;
  margin: 0 0 24px;
}
.search-box {
  max-width: 600px; margin: 0 auto;
  display: flex; align-items: center; gap: 12px;
  background: #2C2C35; border: 1px solid rgba(255,255,255,0.08);
  border-radius: 16px; padding: 0 24px; height: 56px;
}
.search-box:focus-within { border-color: #F58425; }
.search-box svg { width: 20px; height: 20px; color: #92929D; flex-shrink: 0; }
.search-box input {
  background: transparent; border: none; color: #FFFFFF; font-size: 16px;
  outline: none; width: 100%; height: 100%;
}
.search-box input::placeholder { color: #92929D; }

/* ── Content ─────────────────────────────────────────────────── */
.help-content {
  display: flex; gap: 32px; margin-bottom: 48px;
}
.categories-sidebar {
  width: 260px; display: flex; flex-direction: column; gap: 8px; flex-shrink: 0;
}
.cat-btn {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 16px; border-radius: 12px; background: #1C1C24;
  border: 1px solid rgba(255,255,255,0.04); color: #92929D;
  font-size: 14px; font-weight: 600; text-align: left; cursor: pointer;
  transition: all 0.2s;
}
.cat-btn:hover { background: rgba(255,255,255,0.02); color: #E2E8F0; }
.cat-btn.active {
  background: rgba(245,132,37,0.12); color: #F58425; border-color: rgba(245,132,37,0.2);
}
.cat-btn svg { width: 18px; height: 18px; }

/* ── Articles ────────────────────────────────────────────────── */
.articles-grid {
  flex: 1; display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px; align-content: flex-start;
}
.article-card {
  background: #1C1C24; border: 1px solid rgba(255,255,255,0.04);
  border-radius: 16px; padding: 24px;
  display: flex; flex-direction: column;
  transition: transform 0.2s; cursor: pointer;
}
.article-card:hover { border-color: rgba(255,255,255,0.1); transform: translateY(-2px); }
.article-card h4 {
  font-size: 16px; font-weight: 600; color: #FFFFFF; margin: 0 0 12px; line-height: 1.4;
}
.article-card p {
  color: #92929D; font-size: 14px; line-height: 1.5; margin: 0 0 20px; flex: 1;
}
.read-more {
  background: none; border: none; color: #F58425; font-size: 13px; font-weight: 600;
  padding: 0; text-align: left; cursor: pointer;
}

/* ── Support Banner ──────────────────────────────────────────── */
.support-banner {
  background: #1C1C24; border: 1px solid rgba(255,255,255,0.04);
  border-radius: 16px; padding: 32px 48px;
  display: flex; justify-content: space-between; align-items: center;
}
.support-text h3 { font-size: 20px; font-weight: 700; color: #FFFFFF; margin: 0 0 8px; }
.support-text p { color: #92929D; font-size: 14px; margin: 0; }
.btn-support {
  padding: 14px 28px; border-radius: 12px;
  background: #FFFFFF; border: none; color: #1C1C24;
  font-size: 15px; font-weight: 700; cursor: pointer;
  transition: opacity 0.2s;
}
.btn-support:hover { opacity: 0.9; }
</style>
