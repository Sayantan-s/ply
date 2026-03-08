<script setup lang="ts">
import { inject } from "vue";
import { AnimatePresence, Motion } from "motion-v";
import { MatrixLoader } from "@/components/atoms";
import StatusMessage from "../../molecules/StatusMessage/StatusMessage.vue";
import { STREAMING_REPORT_CONTEXT_KEY } from "./streaming-report.context";
import { CheckCircle2, CircleSlash } from "lucide-vue-next";

const ctx = inject(STREAMING_REPORT_CONTEXT_KEY)!;
</script>

<template>
  <AnimatePresence>
    <Motion
      v-if="ctx.currentStatus.value"
      key="status"
      as="div"
      class="streaming-report-status"
      :initial="{ opacity: 0, y: -8 }"
      :animate="{ opacity: 1, y: 0 }"
      :exit="{ opacity: 0, y: -8 }"
      :transition="{ type: 'spring', stiffness: 300, damping: 24 }"
    >
      <MatrixLoader
        v-if="
          ctx.currentStatus.value !== 'fumbled' &&
          ctx.currentStatus.value !== 'locked_in'
        "
        variant="text"
        size="md"
        tone="accent"
      />
      <CheckCircle2
        v-if="ctx.currentStatus.value === 'locked_in'"
        class="status-icon status-icon--success"
      />
      <CircleSlash
        v-if="ctx.currentStatus.value === 'fumbled'"
        class="status-icon status-icon--error"
      />
      <StatusMessage :status="ctx.currentStatus.value" :is-active="true" />
    </Motion>
  </AnimatePresence>
</template>

<style scoped>
.streaming-report-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-icon {
  width: 1rem;
  height: 1rem;
}

.status-icon--success {
  color: var(--success);
}

.status-icon--error {
  color: var(--error);
}
</style>
