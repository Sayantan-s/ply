<script setup lang="ts">
import { TabsRoot, TabsList } from "reka-ui";

withDefaults(
  defineProps<{
    modelValue: string;
    unmountOnHide?: boolean;
  }>(),
  { unmountOnHide: false },
);

const emit = defineEmits<{
  "update:modelValue": [value: string];
}>();
</script>

<template>
  <TabsRoot
    :model-value="modelValue"
    :unmount-on-hide="unmountOnHide"
    @update:model-value="emit('update:modelValue', $event as string)"
  >
    <TabsList class="tab-bar">
      <slot name="triggers" />
    </TabsList>
    <slot />
  </TabsRoot>
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
