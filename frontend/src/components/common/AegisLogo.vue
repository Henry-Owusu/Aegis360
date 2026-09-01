<script setup lang="ts">
interface Props {
  height?: number
}

withDefaults(defineProps<Props>(), {
  height: 225,
})
</script>

<template>
  <div class="aegis-logo-container">
    <img src="/Aegislogo.jpeg" alt="Aegis360 Logo" class="logo-image" :style="{ height: `62px` }" />
  </div>
</template>

<style scoped>
.aegis-logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 4px 0;
}

.logo-image {
  max-width: 100%;
  object-fit: contain;
  filter: drop-shadow(0 4px 12px rgba(13, 148, 136, 0.08));
  transition: transform 0.3s ease;
}

.logo-image:hover {
  transform: scale(1.02);
}
</style>
