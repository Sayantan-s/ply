<script setup lang="ts">
import { ToggleGroupRoot } from "reka-ui";

withDefaults(
  defineProps<{
    modelValue?: string;
    type?: "single";
    disabled?: boolean;
  }>(),
  { type: "single", disabled: false },
);

const emit = defineEmits<{
  "update:modelValue": [value: string];
}>();
</script>

<template>
  <ToggleGroupRoot
    :model-value="modelValue"
    :type="type"
    :disabled="disabled"
    class="toggle-group"
    @update:model-value="emit('update:modelValue', ($event as string) ?? '')"
  >
    <slot />
  </ToggleGroupRoot>
</template>

<style scoped>
.toggle-group {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
</style>
