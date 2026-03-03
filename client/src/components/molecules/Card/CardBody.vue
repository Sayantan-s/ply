<script setup lang="ts">
</script>

<template>
  <div class="card-body">
    <slot />
  </div>
</template>

<style scoped>
.card-body {
  background: var(--surface);
  padding: 10px 12px;
  width: 100%;
  font-family: var(--font);
  font-size: 11px;
  font-weight: 400;
  color: #777788;
  line-height: 1.5;
}
</style>
