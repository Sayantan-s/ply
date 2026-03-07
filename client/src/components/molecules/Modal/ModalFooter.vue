<script setup lang="ts">
</script>

<template>
  <div class="modal-footer">
    <slot />
  </div>
</template>

<style scoped>
.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-top: 1px solid var(--surface);
}
</style>
