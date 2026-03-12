<script setup lang="ts">
import { ScanSearch, CircleHelp } from "lucide-vue-next";

defineProps<{
  activeStep?: number;
}>();

const steps = [
  { num: 1, label: "01_upload" },
  { num: 2, label: "02_details" },
  { num: 3, label: "03_review" },
];
</script>

<template>
  <header class="wizard-nav">
    <div class="wizard-nav__logo">
      <ScanSearch :size="20" class="wizard-nav__logo-icon" />
      <span class="wizard-nav__logo-text">jd_match</span>
    </div>
    <nav class="wizard-nav__steps">
      <template v-for="(step, i) in steps" :key="step.num">
        <span
          class="wizard-nav__step"
          :class="{ 'wizard-nav__step--active': step.num === activeStep }"
        >
          {{ step.label }}
        </span>
        <span v-if="i < steps.length - 1" class="wizard-nav__line" />
      </template>
    </nav>
    <div class="wizard-nav__right">
      <CircleHelp :size="20" class="wizard-nav__icon" />
    </div>
  </header>
</template>

<style scoped>
.wizard-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 3.5rem;
  padding: 0 2.5rem;
  border-bottom: 1px solid #e2e2e2;
  width: 100%;
  flex-shrink: 0;
  background-color: var(--bg);
}

.wizard-nav__logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.wizard-nav__logo-icon {
  color: var(--fg);
}

.wizard-nav__logo-text {
  font-family: var(--font);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: -0.03125rem;
  color: var(--fg);
}

.wizard-nav__steps {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.wizard-nav__step {
  font-family: var(--font);
  font-size: 0.75rem;
  font-weight: 400;
  color: var(--muted);
}

.wizard-nav__step--active {
  font-weight: 600;
  color: var(--fg);
}

.wizard-nav__line {
  display: block;
  width: 2rem;
  height: 1px;
  background: var(--border);
}

.wizard-nav__right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.wizard-nav__icon {
  color: var(--muted);
}

@media (max-width: 640px) {
  .wizard-nav {
    padding: 0 1rem;
  }

  .wizard-nav__steps {
    gap: 0.75rem;
  }

  .wizard-nav__line {
    width: 1rem;
  }

  .wizard-nav__step {
    font-size: 0.625rem;
  }
}
</style>
