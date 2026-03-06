<script setup lang="ts">
import { inject } from "vue";
import { BUTTON_CONTEXT_KEY } from "./button.context";

const ctx = inject(BUTTON_CONTEXT_KEY)!;
</script>

<template>
  <span v-if="!ctx.loading.value" class="button-content">
    <slot />
  </span>
</template>

<style scoped>
.button-content {
  order: 0;
}
</style>
