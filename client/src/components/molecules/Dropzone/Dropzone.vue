<script setup lang="ts">
import { computed, ref } from "vue";
import { Upload } from "lucide-vue-next";

const props = withDefaults(
  defineProps<{
    formats?: string[];
    maxSize?: number;
    multiple?: boolean;
  }>(),
  {
    formats: () => [".pdf", ".docx"],
    maxSize: 10,
    multiple: false,
  },
);

const emit = defineEmits<{
  drop: [files: File[]];
}>();

const isDragOver = ref(false);

const acceptString = computed(() => props.formats.join(","));

const hint = computed(() => {
  const fmts = props.formats.join(" ");
  return `${fmts} — max ${props.maxSize}mb`;
});

function filterValid(raw: File[]): File[] {
  const maxBytes = props.maxSize * 1024 * 1024;
  return raw.filter((f) => {
    const ext = `.${f.name.split(".").pop()?.toLowerCase()}`;
    return props.formats.includes(ext) && f.size <= maxBytes;
  });
}

function handleFiles(raw: File[]) {
  const valid = filterValid(raw);
  if (!valid.length) return;
  emit("drop", props.multiple ? valid : [valid[0]]);
}

function onDragOver(e: DragEvent) {
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
  const input = document.createElement("input");
  input.type = "file";
  input.accept = acceptString.value;
  input.multiple = props.multiple;
  input.onchange = () => handleFiles(Array.from(input.files ?? []));
  input.click();
}
</script>

<template>
  <div
    :class="['dropzone', isDragOver && 'dropzone--active']"
    @dragover="onDragOver"
    @dragleave="onDragLeave"
    @drop="onDrop"
    @click="onClick"
  >
    <Upload class="dropzone__icon" />
    <div class="dropzone__texts">
      <span class="dropzone__primary">drag_and_drop or click</span>
      <span class="dropzone__secondary">{{ hint }}</span>
    </div>
  </div>
</template>

<style scoped>
.dropzone {
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
}

.dropzone--active {
  border-color: var(--accent);
  background: var(--info-bg);
}

.dropzone__icon {
  width: 2rem;
  height: 2rem;
  color: #AAAABC;
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
