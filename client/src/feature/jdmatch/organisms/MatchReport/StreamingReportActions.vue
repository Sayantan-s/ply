<script setup lang="ts">
import { inject, markRaw } from "vue";
import { AnimatePresence, Motion } from "motion-v";
import { Download, Plus } from "lucide-vue-next";
import { Button, ButtonIcon, ButtonContent } from "@/components/atoms";
import { STREAMING_REPORT_CONTEXT_KEY } from "./streaming-report.context";

const ctx = inject(STREAMING_REPORT_CONTEXT_KEY)!;

defineEmits<{
  download: [];
  newMatch: [];
}>();

const DownloadIcon = markRaw(Download);
const PlusIcon = markRaw(Plus);
</script>

<template>
  <AnimatePresence>
    <Motion
      v-if="ctx.isComplete.value"
      key="actions"
      as="div"
      class="streaming-report-actions"
      :initial="{ opacity: 0, y: 12 }"
      :animate="{ opacity: 1, y: 0 }"
      :exit="{ opacity: 0, y: 12 }"
      :transition="{ type: 'spring', stiffness: 260, damping: 20 }"
    >
      <div class="streaming-report-actions__divider" />
      <div class="streaming-report-actions__buttons">
        <Button variant="outline" fluid @click="$emit('download')">
          <ButtonIcon :icon="DownloadIcon" position="pre" :size="14" />
          <ButtonContent>Download Report</ButtonContent>
        </Button>
        <Button variant="primary" fluid @click="$emit('newMatch')">
          <ButtonIcon :icon="PlusIcon" position="pre" :size="14" />
          <ButtonContent>New Match</ButtonContent>
        </Button>
      </div>
    </Motion>
  </AnimatePresence>
</template>

<style scoped>
.streaming-report-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.streaming-report-actions__divider {
  height: 1px;
  background: #e2e2e2;
  width: 100%;
}

.streaming-report-actions__buttons {
  display: flex;
  gap: 0.625rem;
  width: 100%;
}
</style>
