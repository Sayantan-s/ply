<script setup lang="ts">
import { inject } from "vue";
import { Motion } from "motion-v";
import { MatrixLoader } from "@/components/atoms";
import StatusMessage from "../../molecules/StatusMessage/StatusMessage.vue";
import { STREAMING_REPORT_CONTEXT_KEY } from "./streaming-report.context";
import { CheckCircle2, CircleSlash } from "lucide-vue-next";

const ctx = inject(STREAMING_REPORT_CONTEXT_KEY)!;
</script>

<template>
  <div class="streaming-report-status">
    <Motion
      v-if="ctx.currentStatus.value"
      as="div"
      class="streaming-report-status__content"
      :initial="{ opacity: 0 }"
      :animate="{ opacity: 1 }"
      :transition="{ duration: 0.2 }"
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
  </div>
</template>

<style scoped>
.streaming-report-status {
  min-height: 1.5rem;
}

.streaming-report-status__content {
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
