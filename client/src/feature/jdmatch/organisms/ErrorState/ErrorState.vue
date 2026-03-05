<script setup lang="ts">
import { computed, markRaw } from "vue";
import { Motion } from "motion-v";
import { FileX, ZapOff, TriangleAlert, RefreshCw } from "lucide-vue-next";
import { Button } from "@/components/atoms";

const props = defineProps<{
  variant: "upload" | "analysis";
  errorMessage?: string;
  requestId?: string;
}>();

defineEmits<{
  retry: [];
  goBack: [];
}>();

const RefreshIcon = markRaw(RefreshCw);

const icon = computed(() => (props.variant === "upload" ? FileX : ZapOff));

const iconBg = computed(() =>
  props.variant === "upload" ? "var(--error-bg)" : "var(--warning-bg)",
);

const iconColor = computed(() =>
  props.variant === "upload" ? "var(--error)" : "var(--warning)",
);

const title = computed(() =>
  props.variant === "upload" ? "Upload Failed" : "Analysis Failed",
);

const description = computed(() =>
  props.variant === "upload"
    ? "We couldn't process your file. Please check the format and try again."
    : "The matching engine encountered an error during processing.",
);

const detailBg = computed(() =>
  props.variant === "upload" ? "var(--error-bg)" : "var(--warning-bg)",
);

const detailBorder = computed(() =>
  props.variant === "upload" ? "var(--error-border)" : "var(--warning-border)",
);

const detailColor = computed(() =>
  props.variant === "upload" ? "var(--error)" : "var(--warning)",
);
</script>

<template>
  <Motion
    class="error-state"
    :initial="{ opacity: 0, y: 12 }"
    :animate="{ opacity: 1, y: 0 }"
    :transition="{ duration: 0.3 }"
  >
    <div class="error-state__icon" :style="{ background: iconBg }">
      <component :is="icon" :size="28" :style="{ color: iconColor }" />
    </div>

    <div class="error-state__text">
      <h3 class="error-state__title">{{ title }}</h3>
      <p class="error-state__description">{{ description }}</p>
    </div>

    <div
      v-if="errorMessage"
      class="error-state__detail"
      :style="{ background: detailBg, borderColor: detailBorder }"
    >
      <div class="error-state__detail-row">
        <TriangleAlert :size="14" :style="{ color: detailColor }" />
        <span class="error-state__detail-text" :style="{ color: detailColor }">
          {{ errorMessage }}
        </span>
      </div>
      <span v-if="requestId" class="error-state__request-id">
        request_id: {{ requestId }}
      </span>
    </div>

    <div class="error-state__actions">
      <Button variant="primary" fluid @click="$emit('retry')">
        <component :is="RefreshIcon" :size="14" />
        {{ variant === "upload" ? "Try Again" : "Retry Analysis" }}
      </Button>
      <Button variant="ghost" fluid @click="$emit('goBack')">
        {{ variant === "upload" ? "Go Back" : "Start Over" }}
      </Button>
    </div>
  </Motion>
</template>

<style scoped>
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.75rem;
  width: 100%;
}

.error-state__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 4rem;
  height: 4rem;
}

.error-state__text {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
}

.error-state__title {
  font-family: var(--font);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--fg);
}

.error-state__description {
  font-family: var(--font);
  font-size: 0.75rem;
  font-weight: 400;
  line-height: 1.5;
  color: #777788;
  text-align: center;
}

.error-state__detail {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  width: 100%;
  padding: 0.75rem 0.875rem;
  border: 1px solid;
}

.error-state__detail-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.error-state__detail-text {
  font-family: var(--font);
  font-size: 0.6875rem;
  font-weight: 400;
}

.error-state__request-id {
  font-family: var(--font);
  font-size: 0.625rem;
  font-weight: 400;
  color: var(--muted);
}

.error-state__actions {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  width: 100%;
}
</style>
