<script setup lang="ts">
</script>

<template>
  <div class="card">
    <slot />
  </div>
</template>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  border: 1px solid var(--border);
  width: 350px;
}
</style>
