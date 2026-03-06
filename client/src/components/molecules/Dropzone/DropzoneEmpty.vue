<script setup lang="ts">
import { inject } from "vue";
import { Motion, AnimatePresence } from "motion-v";
import { Upload } from "lucide-vue-next";
import { DROPZONE_CONTEXT_KEY } from "./dropzone.context";

const ctx = inject(DROPZONE_CONTEXT_KEY)!;

console.log("render....");
</script>

<template>
  <AnimatePresence>
    <Motion
      v-if="!ctx.hasFiles.value"
      key="empty"
      class="dropzone__empty"
      :initial="{ opacity: 0, y: 8 }"
      :animate="{ opacity: 1, y: 0 }"
      :exit="{ opacity: 0, y: -8 }"
      :transition="{ duration: 0.2 }"
    >
      <Motion
        as="span"
        class="dropzone__icon-wrap"
        :animate="
          ctx.isDragOver.value ? { y: -4, scale: 1.1 } : { y: 0, scale: 1 }
        "
        :transition="{ type: 'spring', stiffness: 300, damping: 20 }"
      >
        <Upload class="dropzone__icon" />
      </Motion>
      <div class="dropzone__texts">
        <span class="dropzone__primary">drag_and_drop or click</span>
        <span class="dropzone__secondary">{{ ctx.hint.value }}</span>
      </div>
    </Motion>
  </AnimatePresence>
</template>

<style scoped>
.dropzone__empty {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.875rem;
}

.dropzone__icon-wrap {
  display: inline-flex;
}

.dropzone__icon {
  width: 2rem;
  height: 2rem;
  color: #aaaabc;
}

.dropzone__texts {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.dropzone__primary {
  font-family: var(--font);
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--fg);
  text-align: center;
}

.dropzone__secondary {
  font-family: var(--font);
  font-size: 0.625rem;
  font-weight: 400;
  color: var(--muted);
  text-align: center;
}
</style>
