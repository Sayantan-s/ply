<script setup lang="ts">
defineProps<{
  label: string;
  placeholder?: string;
}>();

const model = defineModel<string>({ default: "" });
</script>

<template>
  <div class="textarea-wrapper">
    <label class="textarea-label">{{ label }}</label>
    <div class="textarea-box">
      <textarea
        v-model="model"
        :placeholder="placeholder"
        class="textarea-field"
      />
    </div>
  </div>
</template>

<style scoped>
.textarea-wrapper {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 300px;
}

.textarea-label {
  font-family: var(--font);
  font-size: 11px;
  font-weight: 600;
  color: var(--fg);
}

.textarea-box {
  background: #fff;
  border: 1px solid var(--border);
  padding: 12px 14px;
  width: 100%;
  min-height: 140px;
}

.textarea-field {
  border: none;
  outline: none;
  background: transparent;
  font-family: var(--font);
  font-size: 12px;
  font-weight: 400;
  color: var(--fg);
  line-height: 1.6;
  width: 100%;
  height: 100%;
  min-height: 116px;
  resize: vertical;
}

.textarea-field::placeholder {
  color: var(--muted);
}
</style>
