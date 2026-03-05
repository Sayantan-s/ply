<script setup lang="ts">
import { ScanSearch, CircleHelp, ArrowLeft, Share2, Download, LifeBuoy } from "lucide-vue-next";

const props = defineProps<{
  variant: "wizard" | "report" | "empty";
  activeStep?: number;
  navTitle?: string;
}>();

defineEmits<{
  back: [];
  share: [];
  download: [];
}>();

const steps = [
  { num: 1, label: "01_upload" },
  { num: 2, label: "02_details" },
  { num: 3, label: "03_review" },
];
</script>

<template>
  <header class="wizard-nav">
    <!-- Wizard variant: logo + breadcrumb steps + help -->
    <template v-if="variant === 'wizard'">
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
    </template>

    <!-- Report variant: back + breadcrumb title + share/download -->
    <template v-else-if="variant === 'report'">
      <div class="wizard-nav__left">
        <button class="wizard-nav__back-btn" aria-label="Go back" @click="$emit('back')">
          <ArrowLeft :size="20" />
        </button>
        <span class="wizard-nav__logo-text">jd_match</span>
        <span class="wizard-nav__slash">/</span>
        <span class="wizard-nav__title">{{ navTitle ?? "match_report" }}</span>
      </div>
      <div class="wizard-nav__right">
        <button class="wizard-nav__icon-btn" aria-label="Share" @click="$emit('share')">
          <Share2 :size="20" class="wizard-nav__icon" />
        </button>
        <button class="wizard-nav__icon-btn" aria-label="Download" @click="$emit('download')">
          <Download :size="20" class="wizard-nav__icon" />
        </button>
      </div>
    </template>

    <!-- Empty variant: back + breadcrumb title + help -->
    <template v-else>
      <div class="wizard-nav__left">
        <button class="wizard-nav__back-btn" aria-label="Go back" @click="$emit('back')">
          <ArrowLeft :size="20" />
        </button>
        <span class="wizard-nav__logo-text">jd_match</span>
        <span class="wizard-nav__slash">/</span>
        <span class="wizard-nav__title">{{ navTitle ?? "no_results" }}</span>
      </div>
      <div class="wizard-nav__right">
        <LifeBuoy :size="20" class="wizard-nav__icon" />
      </div>
    </template>
  </header>
</template>

<style scoped>
.wizard-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 3.5rem;
  padding: 0 2.5rem;
  background: var(--bg);
  border-bottom: 1px solid #e2e2e2;
  width: 100%;
  flex-shrink: 0;
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

.wizard-nav__left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.wizard-nav__back-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--fg);
  padding: 0;
}

.wizard-nav__slash {
  font-family: var(--font);
  font-size: 1rem;
  font-weight: 400;
  color: var(--border);
}

.wizard-nav__title {
  font-family: var(--font);
  font-size: 0.875rem;
  font-weight: 400;
  color: #777788;
}

.wizard-nav__icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

.wizard-nav__icon-btn:hover .wizard-nav__icon {
  color: var(--fg);
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
