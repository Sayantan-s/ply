<script setup lang="ts">
import { computed } from "vue";
import { Motion } from "motion-v";

const props = withDefaults(
  defineProps<{
    value: number;
    label?: string;
  }>(),
  { label: "percent" },
);

const size = 120;
const strokeWidth = 9;
const radius = (size - strokeWidth) / 2;
const circumference = 2 * Math.PI * radius;

const dashOffset = computed(() => {
  const clamped = Math.min(100, Math.max(0, props.value));
  return circumference * (1 - clamped / 100);
});
</script>

<template>
  <div class="score-ring">
    <svg :width="size" :height="size" class="score-ring__svg">
      <circle
        class="score-ring__track"
        :cx="size / 2"
        :cy="size / 2"
        :r="radius"
        fill="none"
        :stroke-width="strokeWidth"
      />
      <Motion
        as="circle"
        class="score-ring__progress"
        :cx="size / 2"
        :cy="size / 2"
        :r="radius"
        fill="none"
        :stroke-width="strokeWidth"
        :stroke-dasharray="circumference"
        :initial="{ strokeDashoffset: circumference }"
        :animate="{ strokeDashoffset: dashOffset }"
        :transition="{ duration: 1, type: 'tween' }"
        stroke-linecap="round"
        :transform="`rotate(-90 ${size / 2} ${size / 2})`"
      />
    </svg>
    <div class="score-ring__value-wrap">
      <span class="score-ring__value">{{ value }}</span>
      <span class="score-ring__unit">{{ label }}</span>
    </div>
  </div>
</template>

<style scoped>
.score-ring {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 7.5rem;
  height: 7.5rem;
}

.score-ring__svg {
  position: absolute;
  inset: 0;
}

.score-ring__track {
  stroke: var(--surface);
}

.score-ring__progress {
  stroke: var(--accent);
}

.score-ring__value-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.125rem;
  z-index: 1;
}

.score-ring__value {
  font-family: var(--font);
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -0.0625rem;
  color: var(--fg);
  text-align: center;
}

.score-ring__unit {
  font-family: var(--font);
  font-size: 0.5625rem;
  font-weight: 600;
  color: var(--muted);
  text-align: center;
}
</style>
