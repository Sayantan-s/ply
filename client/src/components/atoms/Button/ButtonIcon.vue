<script setup lang="ts">
import { inject } from "vue";
import type { Component } from "vue";
import { BUTTON_CONTEXT_KEY } from "./button.context";

const props = withDefaults(
  defineProps<{
    icon: Component;
    position?: "pre" | "post";
    size?: number;
  }>(),
  { position: "pre", size: 16 },
);

const ctx = inject(BUTTON_CONTEXT_KEY)!;
</script>

<template>
  <component
    v-if="!ctx.loading.value"
    :is="props.icon"
    :size="props.size"
    class="button-icon"
    :class="props.position === 'pre' ? 'button-icon--pre' : 'button-icon--post'"
  />
</template>

<style scoped>
.button-icon {
  flex-shrink: 0;
}

.button-icon--pre {
  order: -1;
}

.button-icon--post {
  order: 1;
}
</style>
