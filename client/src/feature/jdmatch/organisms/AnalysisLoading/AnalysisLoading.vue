<script setup lang="ts">
import { MatrixLoader } from "@/components/atoms";
import StatusMessage from "../../molecules/StatusMessage/StatusMessage.vue";
import type { JdMatchStatus } from "../../types/api";

defineProps<{
  statusHistory: readonly JdMatchStatus[];
  currentStatus: JdMatchStatus | null;
}>();
</script>

<template>
  <div class="analysis-loading">
    <div class="analysis-loading__statuses">
      <StatusMessage
        v-for="(status, i) in statusHistory"
        :key="i"
        :status="status"
        :is-active="status === currentStatus"
      />
    </div>
    <div class="analysis-loading__loader">
      <MatrixLoader variant="grid" size="md" tone="accent" />
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
  flex-direction: column;
  width: 100%;
}

.analysis-loading__loader {
  display: flex;
  justify-content: center;
}
</style>
