<script setup lang="ts">
</script>

<template>
  <div class="jd-form">
    <slot name="text-field" />
    <slot name="url-field" />
  </div>
</template>

<style scoped>
.jd-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  width: 100%;
}
</style>
