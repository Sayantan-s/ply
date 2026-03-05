<script setup lang="ts">
import { Briefcase, CircleCheck } from "lucide-vue-next";

defineProps<{
  jdPreview: string;
}>();
</script>

<template>
  <div class="review-card">
    <Briefcase :size="20" class="review-card__icon" />
    <div class="review-card__info">
      <span class="review-card__label">Job Description</span>
      <span class="review-card__detail">{{ jdPreview }}</span>
    </div>
    <CircleCheck :size="18" class="review-card__check" />
  </div>
</template>

<style scoped>
.review-card {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 1rem;
  border: 1px solid var(--border);
  width: 100%;
}

.review-card__icon {
  color: var(--accent);
  flex-shrink: 0;
}

.review-card__info {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  flex: 1;
  min-width: 0;
}

.review-card__label {
  font-family: var(--font);
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--fg);
}

.review-card__detail {
  font-family: var(--font);
  font-size: 0.6875rem;
  font-weight: 400;
  color: var(--muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.review-card__check {
  color: var(--success);
  flex-shrink: 0;
}
</style>
