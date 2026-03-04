<script setup lang="ts">
import { ScanSearch } from "lucide-vue-next";

defineProps<{
  stepLabel?: string;
}>();
</script>

<template>
  <header class="header">
    <div class="header__logo">
      <ScanSearch class="header__logo-icon" />
      <span class="header__logo-text">jd_match</span>
    </div>
    <div class="header__right">
      <slot>
        <span v-if="stepLabel" class="header__step">{{ stepLabel }}</span>
      </slot>
    </div>
  </header>
</template>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 3.25rem;
  padding: 0 1.25rem;
  border-bottom: 1px solid #e2e2e2;
  width: 100%;
}

.header__logo {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.header__logo-icon {
  width: 1.125rem;
  height: 1.125rem;
  color: var(--fg);
}

.header__logo-text {
  font-family: var(--font);
  font-size: 0.875rem;
  font-weight: 600;
  letter-spacing: -0.03125rem;
  color: var(--fg);
}

.header__right {
  display: flex;
  align-items: center;
}

.header__step {
  font-family: var(--font);
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--muted);
}
</style>
