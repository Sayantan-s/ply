<script setup lang="ts">
import { ArrowLeft, Share2, Download } from "lucide-vue-next";

defineProps<{
  title?: string;
}>();

defineEmits<{
  back: [];
  download: [];
}>();
</script>

<template>
  <header class="wizard-nav">
    <div class="wizard-nav__left">
      <button class="wizard-nav__back-btn" aria-label="Go back" @click="$emit('back')">
        <ArrowLeft :size="20" />
      </button>
      <span class="wizard-nav__logo-text">jd_match</span>
      <span class="wizard-nav__slash">/</span>
      <span class="wizard-nav__title">{{ title ?? "match_report" }}</span>
    </div>
    <div class="wizard-nav__right">
      <button class="wizard-nav__icon-btn" aria-label="Share">
        <Share2 :size="20" class="wizard-nav__icon" />
      </button>
      <button class="wizard-nav__icon-btn" aria-label="Download" @click="$emit('download')">
        <Download :size="20" class="wizard-nav__icon" />
      </button>
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
  background: var(--bg);
  border-bottom: 1px solid #e2e2e2;
  width: 100%;
  flex-shrink: 0;
}

.wizard-nav__logo-text {
  font-family: var(--font);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: -0.03125rem;
  color: var(--fg);
}

.wizard-nav__left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.wizard-nav__right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.wizard-nav__icon {
  color: var(--muted);
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
}
</style>
