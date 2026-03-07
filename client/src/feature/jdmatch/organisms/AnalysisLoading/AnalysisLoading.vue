<script setup lang="ts">
import { MatrixLoader } from "@/components/atoms";
import StatusMessage from "../../molecules/StatusMessage/StatusMessage.vue";
import type { JdMatchStatus } from "../../types/api";
import { computed, type ComputedRef } from "vue";
import type { LoaderVariants } from "@/components/atoms/MatrixLoader/MatrixLoader.vue";

const props = defineProps<{
  statusHistory: readonly JdMatchStatus[];
  currentStatus: JdMatchStatus | null;
}>();

const TONE = computed(() => ({
  locked_in: "success",
  fumbled: "danger",
}));

const tone: ComputedRef<NonNullable<LoaderVariants["tone"]>> = computed(() =>
  props.currentStatus ? TONE.value[props.currentStatus] : "accent",
);
</script>

<template>
  <div class="analysis-loading">
    <div class="analysis-loading__statuses">
      <MatrixLoader variant="text" size="md" :tone="tone" />
      <StatusMessage :status="currentStatus!" :is-active="true" />
    </div>
  </div>
</template>

<style scoped>
.analysis-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  padding: 2rem 0;
  width: 100%;
}

.analysis-loading__statuses {
  display: flex;
  width: 100%;
  align-items: center;
  gap: 0.5rem;
}

.analysis-loading__loader {
  display: flex;
  justify-content: center;
}
</style>
