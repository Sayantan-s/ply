<script setup lang="ts">
</script>

<template>
  <div class="modal-body">
    <slot />
  </div>
</template>

<style scoped>
.modal-body {
  padding: 1.25rem;
  overflow-y: auto;
  max-height: 60vh;
  font-family: var(--font);
  font-size: 0.8125rem;
  color: var(--fg);
  line-height: 1.6;
}
</style>
