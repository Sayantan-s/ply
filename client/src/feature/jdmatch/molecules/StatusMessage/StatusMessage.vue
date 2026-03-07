<script setup lang="ts">
import { computed } from "vue";
import { Motion } from "motion-v";
import type { JdMatchStatus } from "../../types/api";

const props = defineProps<{
  status: JdMatchStatus;
  isActive: boolean;
}>();

const labelMap: Record<JdMatchStatus, string> = {
  warming_up: "Warming up...",
  lining_up: "Lining up...",
  churning: "Churning...",
  combing: "Combing through details...",
  pondering: "Pondering...",
  cooking: "Cooking...",
  locked_in: "Brewed!",
  fumbled: "Slipped!",
};

const label = computed(() => labelMap[props.status]);
const isFinal = computed(
  () => props.status === "locked_in" || props.status === "fumbled",
);
const isError = computed(() => props.status === "fumbled");
</script>

<template>
  <Motion
    :initial="{ opacity: 0, y: 8 }"
    :animate="{ opacity: 1, y: 0 }"
    :transition="{ duration: 0.3 }"
    :class="[
      'status-message',
      isActive && 'status-message--active',
      isFinal && 'status-message--final',
      isError && 'status-message--error',
    ]"
  >
    <span class="status-message__label">{{ label }}</span>
  </Motion>
</template>

<style scoped>
.status-message {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.375rem 0;
  font-family: var(--font);
  font-size: 0.75rem;
  font-weight: 400;
  color: var(--muted);
}

.status-message--active {
  color: var(--accent);
  font-weight: 600;
}

.status-message--final {
  color: var(--success);
}

.status-message--error {
  color: var(--error);
}

.status-message__dot {
  width: 0.375rem;
  height: 0.375rem;
  border-radius: 50%;
  background: currentColor;
  flex-shrink: 0;
}

.status-message__label {
  line-height: 1.4;
}
</style>
