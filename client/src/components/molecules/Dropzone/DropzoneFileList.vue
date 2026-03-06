<script setup lang="ts">
import { inject } from "vue";
import { Motion, AnimatePresence } from "motion-v";
import { FileText, X } from "lucide-vue-next";
import { DROPZONE_CONTEXT_KEY } from "./dropzone.context";

const ctx = inject(DROPZONE_CONTEXT_KEY)!;

console.log("render filelist....");
</script>

<template>
  <AnimatePresence>
    <Motion
      v-if="ctx.hasFiles.value"
      key="files"
      class="dropzone__files"
      :initial="{ opacity: 0, y: 8 }"
      :animate="{ opacity: 1, y: 0 }"
      :exit="{ opacity: 0, y: -8 }"
      :transition="{ duration: 0.2 }"
    >
      <div
        v-for="(file, i) in ctx.acceptedFiles.value"
        :key="file.name"
        class="dropzone__file"
      >
        <FileText class="dropzone__file-icon" />
        <span class="dropzone__file-name">{{ file.name }}</span>
        <span class="dropzone__file-size">{{ ctx.formatSize(file.size) }}</span>
        <button class="dropzone__file-remove" @click.stop="ctx.removeFile(i)">
          <X class="dropzone__remove-icon" />
        </button>
      </div>
      <span class="dropzone__secondary">click to replace</span>
    </Motion>
  </AnimatePresence>
</template>

<style scoped>
.dropzone__files {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 1.25rem;
}

.dropzone__file {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.5rem 0.75rem;
  background: #fff;
  border: 1px solid var(--border);
}

.dropzone__file-icon {
  width: 1rem;
  height: 1rem;
  color: var(--accent);
  flex-shrink: 0;
}

.dropzone__file-name {
  font-family: var(--font);
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--fg);
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropzone__file-size {
  font-family: var(--font);
  font-size: 0.625rem;
  font-weight: 400;
  color: var(--muted);
  flex-shrink: 0;
}

.dropzone__file-remove {
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.125rem;
  flex-shrink: 0;
}

.dropzone__remove-icon {
  width: 0.75rem;
  height: 0.75rem;
  color: var(--muted);
}

.dropzone__file-remove:hover .dropzone__remove-icon {
  color: var(--error);
}

.dropzone__secondary {
  font-family: var(--font);
  font-size: 0.625rem;
  font-weight: 400;
  color: var(--muted);
  text-align: center;
}
</style>
