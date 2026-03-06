<script setup lang="ts">
import { computed, provide, ref } from "vue";
import { DROPZONE_CONTEXT_KEY } from "./dropzone.context";

const props = withDefaults(
  defineProps<{
    modelValue?: File[];
    formats?: string[];
    maxSize?: number;
    multiple?: boolean;
    disabled?: boolean;
  }>(),
  {
    modelValue: undefined,
    formats: () => [".pdf", ".docx"],
    maxSize: 10,
    multiple: false,
    disabled: false,
  },
);

const emit = defineEmits<{
  "update:modelValue": [files: File[]];
  drop: [files: File[]];
}>();

const isDragOver = ref(false);
const internalFiles = ref<File[]>([]);

const isControlled = computed(() => props.modelValue !== undefined);
const acceptedFiles = computed(() =>
  isControlled.value ? props.modelValue! : internalFiles.value,
);
const acceptString = computed(() => props.formats.join(","));
const hint = computed(() => {
  const fmts = props.formats.join(" ");
  return `${fmts} — max ${props.maxSize}mb`;
});
const hasFiles = computed(() => acceptedFiles.value.length > 0);
const isDisabled = computed(() => props.disabled);

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
  if (isControlled.value) {
    emit("update:modelValue", result);
  } else {
    internalFiles.value = result;
  }
  emit("drop", result);
}

function removeFile(index: number) {
  if (isControlled.value) {
    const next = [...acceptedFiles.value];
    next.splice(index, 1);
    emit("update:modelValue", next);
    emit("drop", next);
  } else {
    internalFiles.value.splice(index, 1);
    emit("drop", [...internalFiles.value]);
  }
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

provide(DROPZONE_CONTEXT_KEY, {
  isDragOver,
  hasFiles,
  acceptedFiles,
  hint,
  disabled: isDisabled,
  removeFile,
  formatSize,
});
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
      <slot />
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
  border: 1px dashed var(--border);
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
</style>
