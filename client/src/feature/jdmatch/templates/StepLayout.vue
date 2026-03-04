<script setup lang="ts">
import { AppHeader } from "@/components/organisms";

defineProps<{
  stepLabel?: string | null;
}>();
</script>

<template>
  <div class="step-layout">
    <AppHeader :step-label="stepLabel ?? undefined">
      <template #default>
        <slot name="header-right" />
      </template>
    </AppHeader>
    <main class="step-layout__content">
      <slot />
    </main>
    <footer v-if="$slots.footer" class="step-layout__footer">
      <slot name="footer" />
    </footer>
  </div>
</template>

<style scoped>
.step-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
}

.step-layout__content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  flex: 1;
  width: 100%;
  max-width: 28rem;
  margin: 0 auto;
  padding: 1.5rem 1.25rem;
}

.step-layout__footer {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%;
  max-width: 28rem;
  margin: 0 auto;
  padding: 0 1.25rem 1.5rem;
}

@media (max-width: 640px) {
  .step-layout__content,
  .step-layout__footer {
    max-width: 100%;
  }
}
</style>
