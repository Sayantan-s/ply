<script setup lang="ts">
defineProps<{
  cardWidth?: number;
  noCard?: boolean;
}>();
</script>

<template>
  <div class="step-layout">
    <slot name="nav" />
    <main class="step-layout__body">
      <div
        v-if="!noCard"
        class="step-layout__card"
        :style="cardWidth ? { width: `${cardWidth}px` } : undefined"
      >
        <slot />
      </div>
      <slot v-else />
    </main>
  </div>
</template>

<style scoped>
.step-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  background: var(--surface);
}

.step-layout__body {
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
  padding: 2.5rem;
}

.step-layout__card {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
  width: 32.5rem;
  padding: 2.5rem;
  background: var(--bg);
  border: 1px solid #e2e2e2;
}

@media (max-width: 640px) {
  .step-layout__body {
    padding: 1.25rem;
    align-items: flex-start;
  }

  .step-layout__card {
    width: 100%;
    padding: 1.5rem;
  }
}
</style>
