<script setup lang="ts">
import { ref } from "vue";
import { Upload } from "lucide-vue-next";

defineProps<{
  primaryText?: string;
  secondaryText?: string;
}>();

const emit = defineEmits<{
  drop: [files: File[]];
}>();

const isDragOver = ref(false);

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
  const files = Array.from(e.dataTransfer?.files ?? []);
  if (files.length) emit("drop", files);
}

function onClick() {
  const input = document.createElement("input");
  input.type = "file";
  input.accept = ".pdf,.docx";
  input.onchange = () => {
    const files = Array.from(input.files ?? []);
    if (files.length) emit("drop", files);
  };
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
      <span class="dropzone__primary">{{ primaryText ?? "drag_and_drop or click" }}</span>
      <span class="dropzone__secondary">{{ secondaryText ?? ".pdf .docx — max 10mb" }}</span>
    </div>
  </div>
</template>

<style scoped>
.dropzone {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  width: 350px;
  height: 180px;
  background: var(--surface);
  border: 1px solid var(--border);
  cursor: pointer;
}

.dropzone--active {
  border-color: var(--accent);
  background: var(--info-bg);
}

.dropzone__icon {
  width: 32px;
  height: 32px;
  color: #AAAABC;
}

.dropzone__texts {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.dropzone__primary {
  font-family: var(--font);
  font-size: 12px;
  font-weight: 500;
  color: var(--fg);
  text-align: center;
}

.dropzone__secondary {
  font-family: var(--font);
  font-size: 10px;
  font-weight: 400;
  color: var(--muted);
  text-align: center;
}
</style>
