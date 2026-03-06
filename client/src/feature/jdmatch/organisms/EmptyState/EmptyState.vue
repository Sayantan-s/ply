<script setup lang="ts">
import { markRaw } from "vue";
import { Motion } from "motion-v";
import { SearchX, Sparkles, ArrowLeft } from "lucide-vue-next";
import { Button, ButtonIcon, ButtonContent } from "@/components/atoms";

defineEmits<{
  newMatch: [];
  goHome: [];
}>();

const SparklesIcon = markRaw(Sparkles);
const ArrowLeftIcon = markRaw(ArrowLeft);

const suggestions = [
  { num: "01", text: "Upload a more detailed resume" },
  { num: "02", text: "Check that the JD is relevant to your field" },
  { num: "03", text: "Include a job posting URL for better accuracy" },
];
</script>

<template>
  <Motion
    class="empty-state"
    :initial="{ opacity: 0, y: 12 }"
    :animate="{ opacity: 1, y: 0 }"
    :transition="{ duration: 0.3 }"
  >
    <div class="empty-state__icon">
      <SearchX :size="28" class="empty-state__icon-svg" />
    </div>

    <div class="empty-state__text">
      <h3 class="empty-state__title">No Matches Found</h3>
      <p class="empty-state__description">
        The resume and job description don't share enough overlap to generate a report.
      </p>
    </div>

    <div class="empty-state__suggestions">
      <span class="empty-state__suggestions-label">// suggestions</span>
      <div
        v-for="suggestion in suggestions"
        :key="suggestion.num"
        class="empty-state__suggestion"
      >
        <span class="empty-state__suggestion-num">{{ suggestion.num }}</span>
        <span class="empty-state__suggestion-text">{{ suggestion.text }}</span>
      </div>
    </div>

    <div class="empty-state__actions">
      <Button variant="accent" fluid @click="$emit('newMatch')">
        <ButtonIcon :icon="SparklesIcon" position="pre" :size="14" />
        <ButtonContent>Start New Match</ButtonContent>
      </Button>
      <Button variant="ghost" fluid @click="$emit('goHome')">
        <ButtonIcon :icon="ArrowLeftIcon" position="pre" :size="14" />
        <ButtonContent>Back to Home</ButtonContent>
      </Button>
    </div>
  </Motion>
</template>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.75rem;
  width: 100%;
}

.empty-state__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 4rem;
  height: 4rem;
  background: var(--surface);
}

.empty-state__icon-svg {
  color: var(--muted);
}

.empty-state__text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
}

.empty-state__title {
  font-family: var(--font);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--fg);
}

.empty-state__description {
  font-family: var(--font);
  font-size: 0.75rem;
  font-weight: 400;
  line-height: 1.5;
  color: #777788;
  text-align: center;
}

.empty-state__suggestions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
  padding: 1rem;
  background: var(--surface);
  border: 1px solid #e2e2e2;
}

.empty-state__suggestions-label {
  font-family: var(--font);
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--accent);
}

.empty-state__suggestion {
  display: flex;
  align-items: center;
  gap: 0.625rem;
}

.empty-state__suggestion-num {
  font-family: var(--font);
  font-size: 0.6875rem;
  font-weight: 700;
  color: var(--accent);
}

.empty-state__suggestion-text {
  font-family: var(--font);
  font-size: 0.6875rem;
  font-weight: 400;
  color: #444455;
}

.empty-state__actions {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  width: 100%;
}
</style>
