<script setup lang="ts">
import { computed, provide } from "vue";
import { cva, type VariantProps } from "class-variance-authority";
import { Motion } from "motion-v";
import type { JdMatchStatus } from "../../types/api";
import { STREAMING_REPORT_CONTEXT_KEY } from "./streaming-report.context";

const reportVariants = cva("streaming-report", {
  variants: {
    variant: {
      default: "streaming-report--default",
      compact: "streaming-report--compact",
    },
  },
  defaultVariants: { variant: "default" },
});

type ReportVariants = VariantProps<typeof reportVariants>;

const props = withDefaults(
  defineProps<{
    score: number | null;
    matchingSkills: readonly string[] | null;
    missingSkills: readonly string[] | null;
    streamedExplanation: string;
    isExplanationStreaming: boolean;
    currentStatus: JdMatchStatus | null;
    variant?: NonNullable<ReportVariants["variant"]>;
  }>(),
  { variant: "default" },
);

const classes = computed(() => reportVariants({ variant: props.variant }));

provide(STREAMING_REPORT_CONTEXT_KEY, {
  score: computed(() => props.score),
  matchingSkills: computed(() => props.matchingSkills),
  missingSkills: computed(() => props.missingSkills),
  streamedExplanation: computed(() => props.streamedExplanation),
  isExplanationStreaming: computed(() => props.isExplanationStreaming),
  currentStatus: computed(() => props.currentStatus),
  isLoading: computed(() => props.score === null),
  isComplete: computed(() => props.currentStatus === "locked_in"),
});
</script>

<template>
  <Motion
    as="div"
    :class="classes"
    :initial="{ opacity: 0, y: 12 }"
    :animate="{ opacity: 1, y: 0 }"
    :transition="{ type: 'spring', stiffness: 260, damping: 20 }"
  >
    <slot />
  </Motion>
</template>

<style scoped>
.streaming-report {
  display: flex;
  gap: 2.5rem;
  width: 100%;
  max-width: 80rem;
}

.streaming-report--default {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.streaming-report--compact {
  max-width: 32rem;
}

@media (max-width: 768px) {
  .streaming-report {
    max-width: 100%;
  }
}
</style>
