<script setup lang="ts">
import { inject } from "vue";
import { Motion } from "motion-v";
import { ScoreRing } from "@/components/molecules";
import { Text } from "@/components/atoms";
import { STREAMING_REPORT_CONTEXT_KEY } from "./streaming-report.context";

const ctx = inject(STREAMING_REPORT_CONTEXT_KEY)!;

const pulseTransition = {
  duration: 1.2,
  repeat: Infinity,
  repeatType: "reverse" as const,
};
</script>

<template>
  <div class="streaming-report-score">
    <Motion
      v-if="ctx.score.value !== null"
      as="div"
      class="streaming-report-score__content"
      :initial="{ opacity: 0, scale: 0.85 }"
      :animate="{ opacity: 1, scale: 1 }"
      :transition="{ type: 'spring', stiffness: 260, damping: 20 }"
    >
      <ScoreRing :value="ctx.score.value" />
      <Text variant="label">match_score</Text>
    </Motion>

    <div v-else class="streaming-report-score__content">
      <Motion
        as="div"
        class="streaming-report-score__skeleton-ring"
        :animate="{ opacity: [0.15, 0.35] }"
        :transition="pulseTransition"
      />
      <Motion
        as="div"
        class="streaming-report-score__skeleton-bar"
        :animate="{ opacity: [0.15, 0.35] }"
        :transition="pulseTransition"
      />
    </div>
  </div>
</template>

<style scoped>
.streaming-report-score {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem 0;
  background-color: var(--bg);
  height: max-content;
  position: sticky;
  top: 0;
}

.streaming-report-score__content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.streaming-report-score__skeleton-ring {
  width: 7.5rem;
  height: 7.5rem;
  border-radius: 50%;
  background: #e2e2e2;
}

.streaming-report-score__skeleton-bar {
  width: 4rem;
  height: 0.5rem;
  background: #e2e2e2;
  border-radius: 0.1875rem;
}
</style>
