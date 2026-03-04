<script setup lang="ts"></script>

<template>
  <div class="card-body">
    <slot />
  </div>
</template>

<style scoped>
.card-body {
  background: var(--surface);
  padding: 0.625rem 0.75rem;
  width: 100%;
  font-family: var(--font);
  font-size: 0.6875rem;
  font-weight: 400;
  color: #777788;
  line-height: 1.5;
}
</style>
