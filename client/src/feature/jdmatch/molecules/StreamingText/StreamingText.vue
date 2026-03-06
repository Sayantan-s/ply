<script setup lang="ts">
import { Motion } from "motion-v";

defineProps<{
  text: string;
  isStreaming: boolean;
}>();
</script>

<template>
  <span class="streaming-text">
    <span>{{ text }}</span>
    <Motion
      v-if="isStreaming"
      as="span"
      class="streaming-text__cursor"
      :animate="{ opacity: [1, 0] }"
      :transition="{ duration: 0.6, repeat: Infinity, repeatType: 'reverse' }"
    />
  </span>
</template>

<style scoped>
.streaming-text {
  font-family: var(--font);
  font-size: 0.6875rem;
  font-weight: 400;
  line-height: 1.6;
  color: #444455;
  white-space: pre-wrap;
}

.streaming-text__cursor {
  display: inline-block;
  width: 0.125rem;
  height: 0.875rem;
  background: var(--accent);
  margin-left: 0.125rem;
  vertical-align: text-bottom;
}
</style>
