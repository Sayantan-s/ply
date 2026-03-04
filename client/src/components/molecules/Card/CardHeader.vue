<script setup lang="ts">
import type { Component } from "vue";

defineProps<{
  icon?: Component;
  title: string;
}>();
</script>

<template>
  <div class="card-header">
    <div v-if="icon" class="card-header__icon-wrap">
      <component :is="icon" class="card-header__icon" />
    </div>
    <span class="card-header__title">{{ title }}</span>
  </div>
</template>

<style scoped>
.card-header {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  width: 100%;
}

.card-header__icon-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  background: var(--surface);
}

.card-header__icon {
  width: 1rem;
  height: 1rem;
  color: var(--fg);
}

.card-header__title {
  font-family: var(--font);
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--fg);
}
</style>
