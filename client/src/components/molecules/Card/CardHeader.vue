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
  gap: 10px;
  width: 100%;
}

.card-header__icon-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: var(--surface);
}

.card-header__icon {
  width: 16px;
  height: 16px;
  color: var(--fg);
}

.card-header__title {
  font-family: var(--font);
  font-size: 12px;
  font-weight: 600;
  color: var(--fg);
}
</style>
