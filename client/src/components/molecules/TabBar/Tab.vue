<script setup lang="ts">
import { computed, inject, type Component, type ComputedRef } from "vue";

interface TabBarContext {
  activeTab: ComputedRef<string>;
  setTab: (value: string) => void;
}

const props = defineProps<{
  value: string;
  icon?: Component;
  label: string;
}>();

const context = inject<TabBarContext>("tab-bar-context")!;
const isActive = computed(() => context.activeTab.value === props.value);
</script>

<template>
  <button
    :class="['tab', isActive ? 'tab--active' : 'tab--inactive']"
    @click="context.setTab(value)"
  >
    <component v-if="icon" :is="icon" class="tab__icon" />
    <span class="tab__label">{{ label }}</span>
  </button>
</template>

<style scoped>
.tab {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  flex: 1;
  height: 100%;
  border: none;
  cursor: pointer;
  font-family: var(--font);
  font-size: 11px;
  font-weight: 600;
  outline: none;
}

.tab__icon {
  width: 14px;
  height: 14px;
}

.tab--active {
  background: #fff;
  color: var(--fg);
}

.tab--inactive {
  background: transparent;
  color: var(--muted);
}
</style>
