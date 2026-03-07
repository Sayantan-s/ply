<script setup lang="ts">
import { Motion } from "motion-v";

const pulseTransition = {
  duration: 1.2,
  repeat: Infinity,
  repeatType: "reverse" as const,
};
</script>

<template>
  <div class="skeleton">
    <!-- Left Column -->
    <div class="skeleton__left">
      <div class="skeleton__score">
        <Motion
          as="div"
          class="skeleton__ring"
          :animate="{ opacity: [0.15, 0.35] }"
          :transition="pulseTransition"
        />
        <Motion
          as="div"
          class="skeleton__bar skeleton__bar--sm"
          :animate="{ opacity: [0.15, 0.35] }"
          :transition="pulseTransition"
        />
      </div>
      <div class="skeleton__summary">
        <Motion
          as="div"
          class="skeleton__bar skeleton__bar--xs"
          :animate="{ opacity: [0.15, 0.35] }"
          :transition="pulseTransition"
        />
        <Motion
          v-for="i in 4"
          :key="i"
          as="div"
          class="skeleton__bar"
          :style="{ width: i === 4 ? '60%' : '100%' }"
          :animate="{ opacity: [0.15, 0.35] }"
          :transition="{ ...pulseTransition, delay: i * 0.1 }"
        />
      </div>
    </div>

    <!-- Right Column -->
    <div class="skeleton__right">
      <div class="skeleton__section">
        <Motion
          as="div"
          class="skeleton__bar skeleton__bar--title"
          :animate="{ opacity: [0.15, 0.35] }"
          :transition="pulseTransition"
        />
        <Motion
          v-for="i in 3"
          :key="`match-${i}`"
          as="div"
          class="skeleton__chip"
          :animate="{ opacity: [0.15, 0.35] }"
          :transition="{ ...pulseTransition, delay: i * 0.1 }"
        />
      </div>
      <div class="skeleton__section">
        <Motion
          as="div"
          class="skeleton__bar skeleton__bar--title"
          :animate="{ opacity: [0.15, 0.35] }"
          :transition="pulseTransition"
        />
        <Motion
          v-for="i in 2"
          :key="`miss-${i}`"
          as="div"
          class="skeleton__chip"
          :animate="{ opacity: [0.15, 0.35] }"
          :transition="{ ...pulseTransition, delay: i * 0.1 }"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.skeleton {
  display: flex;
  gap: 2.5rem;
  width: 100%;
  max-width: 80rem;
}

.skeleton__left {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
  flex: 0.5;
  flex-shrink: 0;
  background-color: var(--bg);
  padding: 1.25rem;
}

.skeleton__right {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
  flex: 0.5;
  flex-shrink: 0;
  padding: 1.25rem;
}

.skeleton__score {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem 0;
}

.skeleton__ring {
  width: 7.5rem;
  height: 7.5rem;
  border-radius: 50%;
  background: #e2e2e2;
}

.skeleton__summary {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background: var(--info-bg);
  border: 1px solid var(--info-border);
  padding: 1.25rem;
}

.skeleton__bar {
  height: 0.625rem;
  background: #e2e2e2;
  border-radius: 0.1875rem;
  width: 100%;
}

.skeleton__bar--sm {
  width: 4rem;
  height: 0.5rem;
}

.skeleton__bar--xs {
  width: 3rem;
  height: 0.375rem;
}

.skeleton__bar--title {
  width: 6rem;
  height: 0.75rem;
}

.skeleton__section {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.skeleton__chip {
  height: 1.75rem;
  background: #e2e2e2;
  border-radius: 0.25rem;
  width: 80%;
}

@media (max-width: 768px) {
  .skeleton {
    flex-direction: column;
    max-width: 100%;
  }

  .skeleton__left,
  .skeleton__right {
    width: 100%;
  }
}
</style>
