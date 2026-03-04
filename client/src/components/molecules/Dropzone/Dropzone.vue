<script setup lang="ts">
import { computed, ref } from "vue";
import { Motion, AnimatePresence } from "motion-v";
import { Upload, FileText, X } from "lucide-vue-next";

const props = withDefaults(
  defineProps<{
    formats?: string[];
    maxSize?: number;
    multiple?: boolean;
    disabled?: boolean;
  }>(),
  {
    formats: () => [".pdf", ".docx"],
    maxSize: 10,
    multiple: false,
    disabled: false,
  },
);

const emit = defineEmits<{
  drop: [files: File[]];
}>();

const isDragOver = ref(false);
const acceptedFiles = ref<File[]>([]);

const acceptString = computed(() => props.formats.join(","));

const hint = computed(() => {
  const fmts = props.formats.join(" ");
  return `${fmts} — max ${props.maxSize}mb`;
});

const hasFiles = computed(() => acceptedFiles.value.length > 0);

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes}b`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}kb`;
  return `${(bytes / (1024 * 1024)).toFixed(1)}mb`;
}

function filterValid(raw: File[]): File[] {
  const maxBytes = props.maxSize * 1024 * 1024;
  return raw.filter((f) => {
    const ext = `.${f.name.split(".").pop()?.toLowerCase()}`;
    return props.formats.includes(ext) && f.size <= maxBytes;
  });
}

function handleFiles(raw: File[]) {
  if (props.disabled) return;
  const valid = filterValid(raw);
  if (!valid.length) return;
  const result = props.multiple ? valid : [valid[0]];
  acceptedFiles.value = result;
  emit("drop", result);
}

function removeFile(index: number) {
  acceptedFiles.value.splice(index, 1);
  emit("drop", [...acceptedFiles.value]);
}

function onDragOver(e: DragEvent) {
  if (props.disabled) return;
  e.preventDefault();
  isDragOver.value = true;
}

function onDragLeave() {
  isDragOver.value = false;
}

function onDrop(e: DragEvent) {
  e.preventDefault();
  isDragOver.value = false;
  handleFiles(Array.from(e.dataTransfer?.files ?? []));
}

function onClick() {
  if (props.disabled) return;
  const input = document.createElement("input");
  input.type = "file";
  input.accept = acceptString.value;
  input.multiple = props.multiple;
  input.onchange = () => handleFiles(Array.from(input.files ?? []));
  input.click();
}
</script>

<template>
  <div class="dropzone-wrapper">
    <div
      :class="[
        'dropzone',
        isDragOver && 'dropzone--active',
        disabled && 'dropzone--disabled',
      ]"
      @dragover="onDragOver"
      @dragleave="onDragLeave"
      @drop="onDrop"
      @click="onClick"
    >
      <AnimatePresence mode="wait">
        <Motion
          v-if="hasFiles"
          key="files"
          class="dropzone__files"
          :initial="{ opacity: 0, y: 8 }"
          :animate="{ opacity: 1, y: 0 }"
          :exit="{ opacity: 0, y: -8 }"
          :transition="{ duration: 0.2 }"
        >
          <div
            v-for="(file, i) in acceptedFiles"
            :key="file.name"
            class="dropzone__file"
          >
            <FileText class="dropzone__file-icon" />
            <span class="dropzone__file-name">{{ file.name }}</span>
            <span class="dropzone__file-size">{{ formatSize(file.size) }}</span>
            <button
              class="dropzone__file-remove"
              @click.stop="removeFile(i)"
            >
              <X class="dropzone__remove-icon" />
            </button>
          </div>
          <span class="dropzone__secondary">click to replace</span>
        </Motion>

        <Motion
          v-else
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
            :animate="isDragOver ? { y: -4, scale: 1.1 } : { y: 0, scale: 1 }"
            :transition="{ type: 'spring', stiffness: 300, damping: 20 }"
          >
            <Upload class="dropzone__icon" />
          </Motion>
          <div class="dropzone__texts">
            <span class="dropzone__primary">drag_and_drop or click</span>
            <span class="dropzone__secondary">{{ hint }}</span>
          </div>
        </Motion>
      </AnimatePresence>
    </div>
  </div>
</template>

<style scoped>
.dropzone-wrapper {
  width: 100%;
}

.dropzone {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.875rem;
  width: 100%;
  height: 11.25rem;
  background: var(--surface);
  border: 1px solid var(--border);
  cursor: pointer;
  padding: 1.25rem;
  overflow: hidden;
}

.dropzone--active {
  border-color: var(--accent);
  background: var(--info-bg);
}

.dropzone--disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

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
</style>
