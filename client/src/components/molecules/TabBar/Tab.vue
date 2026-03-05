<script setup lang="ts">
import type { Component } from "vue";
import { TabsTrigger } from "reka-ui";

defineProps<{
  value: string;
  icon?: Component;
  label: string;
  disabled?: boolean;
}>();
</script>

<template>
  <TabsTrigger :value="value" :disabled="disabled" class="tab">
    <component v-if="icon" :is="icon" class="tab__icon" />
    <span class="tab__label">{{ label }}</span>
  </TabsTrigger>
</template>

<style scoped>
.tab {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  flex: 1;
  height: 100%;
  border: none;
  cursor: pointer;
  font-family: var(--font);
  font-size: 0.6875rem;
  font-weight: 600;
  outline: none;
}

.tab__icon {
  width: 0.875rem;
  height: 0.875rem;
}

.tab[data-state="active"] {
  background: #fff;
  color: var(--fg);
}

.tab[data-state="inactive"] {
  background: transparent;
  color: var(--muted);
}

.tab[data-disabled] {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
