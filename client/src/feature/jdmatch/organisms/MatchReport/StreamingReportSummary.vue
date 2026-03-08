<script setup lang="ts">
import { inject } from "vue";
import { AnimatePresence, Motion } from "motion-v";
import { Text } from "@/components/atoms";
import StreamingText from "../../molecules/StreamingText/StreamingText.vue";
import { STREAMING_REPORT_CONTEXT_KEY } from "./streaming-report.context";

const ctx = inject(STREAMING_REPORT_CONTEXT_KEY)!;

const pulseTransition = {
  duration: 1.2,
  repeat: Infinity,
  repeatType: "reverse" as const,
};
</script>

<template>
  <div class="streaming-report-summary">
    <Text variant="comment">// summary</Text>

    <AnimatePresence mode="wait">
      <Motion
        v-if="ctx.streamedExplanation.value || ctx.isExplanationStreaming.value"
        key="content"
        as="div"
        :initial="{ opacity: 0, y: 8 }"
        :animate="{ opacity: 1, y: 0 }"
        :exit="{ opacity: 0, y: -8 }"
        :transition="{ duration: 0.25 }"
      >
        <StreamingText
          :text="ctx.streamedExplanation.value"
          :is-streaming="ctx.isExplanationStreaming.value"
        />
      </Motion>

      <Motion
        v-else
        key="skeleton"
        as="div"
        class="streaming-report-summary__skeleton"
        :initial="{ opacity: 0 }"
        :animate="{ opacity: 1 }"
        :exit="{ opacity: 0 }"
        :transition="{ duration: 0.2 }"
      >
        <Motion
          v-for="i in 4"
          :key="`sum-${i}`"
          as="div"
          class="streaming-report-summary__bar"
          :style="{ width: i === 4 ? '60%' : '100%' }"
          :animate="{ opacity: [0.15, 0.35] }"
          :transition="{ ...pulseTransition, delay: i * 0.1 }"
        />
      </Motion>
    </AnimatePresence>
  </div>
</template>

<style scoped>
.streaming-report-summary {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background: var(--info-bg);
  border: 1px solid var(--info-border);
  padding: 1.25rem;
}

.streaming-report-summary__skeleton {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.streaming-report-summary__bar {
  height: 0.625rem;
  background: #e2e2e2;
  border-radius: 0.1875rem;
  width: 100%;
}
</style>
