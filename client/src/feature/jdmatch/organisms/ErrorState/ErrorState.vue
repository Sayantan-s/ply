<script setup lang="ts">
import { computed } from "vue";
import { Motion } from "motion-v";
import { StatusIcon, Heading, Text, Alert, Button } from "@/components/atoms";
import { RefreshCw } from "lucide-vue-next";
import { markRaw } from "vue";

const props = defineProps<{
  variant: "upload" | "analysis";
  errorMessage?: string;
}>();

defineEmits<{
  retry: [];
  goBack: [];
}>();

const RefreshIcon = markRaw(RefreshCw);

const title = computed(() =>
  props.variant === "upload" ? "Upload Failed" : "Analysis Failed",
);

const description = computed(() =>
  props.variant === "upload"
    ? "The file could not be processed. Please check the format and try again."
    : "Something went wrong while processing the match analysis. This is usually temporary.",
);

const alertVariant = computed(() =>
  props.variant === "upload" ? "error" as const : "warning" as const,
);

const statusIconVariant = computed(() =>
  props.variant === "upload" ? "error" as const : "warning" as const,
);

const retryLabel = computed(() =>
  props.variant === "upload" ? "Try Again" : "Retry Analysis",
);

const backLabel = computed(() =>
  props.variant === "upload" ? "Go Back" : "Start Over",
);
</script>

<template>
  <Motion
    class="error-state"
    :initial="{ opacity: 0, y: 12 }"
    :animate="{ opacity: 1, y: 0 }"
    :transition="{ duration: 0.3 }"
  >
    <StatusIcon :variant="statusIconVariant" />
    <Heading :level="3">{{ title }}</Heading>
    <Text variant="muted">{{ description }}</Text>
    <Alert
      v-if="errorMessage"
      :variant="alertVariant"
      :message="errorMessage"
    />
    <div class="error-state__actions">
      <Button variant="primary" fluid @click="$emit('retry')">
        <component :is="RefreshIcon" :size="14" />
        {{ retryLabel }}
      </Button>
      <Button variant="ghost" fluid @click="$emit('goBack')">
        {{ backLabel }}
      </Button>
    </div>
  </Motion>
</template>

<style scoped>
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  text-align: center;
  padding: 2rem 0;
  width: 100%;
}

.error-state__actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: 100%;
  margin-top: 0.75rem;
}
</style>
