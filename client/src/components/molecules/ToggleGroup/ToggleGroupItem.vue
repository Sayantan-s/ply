<script setup lang="ts">
import type { Component } from "vue";
import { ToggleGroupItem } from "reka-ui";

defineProps<{
  value: string;
  icon?: Component;
  label: string;
}>();
</script>

<template>
  <ToggleGroupItem :value="value" class="toggle-group-item">
    <component v-if="icon" :is="icon" class="toggle-group-item__icon" />
    <span class="toggle-group-item__label">{{ label }}</span>
  </ToggleGroupItem>
</template>

<style scoped>
.toggle-group-item {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  padding: 0.5rem 0.875rem;
  font-family: var(--font);
  font-size: 0.625rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  outline: none;
}

.toggle-group-item__icon {
  width: 0.875rem;
  height: 0.875rem;
}

.toggle-group-item[data-state="on"] {
  background: var(--fg);
  color: #fff;
}

.toggle-group-item[data-state="off"] {
  background: transparent;
  color: var(--muted);
  border: 1px solid var(--border);
}

.toggle-group-item[data-disabled] {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
