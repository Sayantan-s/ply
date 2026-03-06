<script setup lang="ts">
import { Heading, Text } from "@/components/atoms";

defineProps<{
  stepComment: string;
  title: string;
  subtitle?: string;
}>();
</script>

<template>
  <div class="step-headline">
    <Text variant="comment">{{ stepComment }}</Text>
    <Heading :level="2">{{ title }}</Heading>
    <Text v-if="subtitle" variant="caption">{{ subtitle }}</Text>
  </div>
</template>

<style scoped>
.step-headline {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
}
</style>
