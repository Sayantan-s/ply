<script setup lang="ts">
import { Motion } from "motion-v";
import { StatusIcon, Heading, Text, Button } from "@/components/atoms";
import { Plus, Download } from "lucide-vue-next";
import { markRaw } from "vue";

defineEmits<{
  newMatch: [];
  download: [];
}>();

const PlusIcon = markRaw(Plus);
const DownloadIcon = markRaw(Download);

const suggestions = [
  "Check that the JD matches your field of expertise",
  "Update your resume with relevant keywords",
  "Try a different job post with broader requirements",
];
</script>

<template>
  <Motion
    class="empty-state"
    :initial="{ opacity: 0, y: 12 }"
    :animate="{ opacity: 1, y: 0 }"
    :transition="{ duration: 0.3 }"
  >
    <StatusIcon variant="empty" />
    <Heading :level="3">No Matches Found</Heading>
    <Text variant="muted">
      The resume and job description don't share enough overlap for a meaningful analysis.
    </Text>

    <div class="empty-state__suggestions">
      <Text variant="comment">// suggestions</Text>
      <ol class="empty-state__list">
        <li v-for="(suggestion, i) in suggestions" :key="i" class="empty-state__item">
          {{ suggestion }}
        </li>
      </ol>
    </div>

    <div class="empty-state__actions">
      <Button variant="accent" fluid @click="$emit('newMatch')">
        <component :is="PlusIcon" :size="14" />
        New Match
      </Button>
      <Button variant="outline" fluid @click="$emit('download')">
        <component :is="DownloadIcon" :size="14" />
        Download Report
      </Button>
    </div>
  </Motion>
</template>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  text-align: center;
  padding: 2rem 0;
  width: 100%;
}

.empty-state__suggestions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%;
  background: var(--surface);
  padding: 1rem;
  text-align: left;
}

.empty-state__list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  padding: 0;
}

.empty-state__item {
  font-family: var(--font);
  font-size: 0.6875rem;
  font-weight: 400;
  color: var(--fg);
  line-height: 1.5;
  padding-left: 0.25rem;
}

.empty-state__item::before {
  content: counter(list-item) ". ";
  counter-increment: list-item;
  font-weight: 600;
  color: var(--muted);
}

.empty-state__actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%;
  margin-top: 0.75rem;
}
</style>
