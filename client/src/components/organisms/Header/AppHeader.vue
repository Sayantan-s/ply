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
  height: 52px;
  padding: 0 20px;
  border-bottom: 1px solid #E2E2E2;
  width: 100%;
}

.header__logo {
  display: flex;
  align-items: center;
  gap: 6px;
}

.header__logo-icon {
  width: 18px;
  height: 18px;
  color: var(--fg);
}

.header__logo-text {
  font-family: var(--font);
  font-size: 14px;
  font-weight: 600;
  letter-spacing: -0.5px;
  color: var(--fg);
}

.header__right {
  display: flex;
  align-items: center;
}

.header__step {
  font-family: var(--font);
  font-size: 11px;
  font-weight: 600;
  color: var(--muted);
}
</style>
