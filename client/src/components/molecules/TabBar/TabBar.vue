<script setup lang="ts">
import { provide, computed } from "vue";

const props = defineProps<{
  modelValue: string;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: string];
}>();

provide("tab-bar-context", {
  activeTab: computed(() => props.modelValue),
  setTab: (value: string) => emit("update:modelValue", value),
});
</script>

<template>
  <div class="tab-bar">
    <slot />
  </div>
</template>

<style scoped>
.tab-bar {
  display: flex;
  width: 100%;
  height: 2.5rem;
  padding: 0.1875rem;
  background: var(--surface);
}
</style>
