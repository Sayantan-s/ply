<script setup lang="ts">
import { computed, ref } from "vue";

const props = withDefaults(
  defineProps<{
    label: string;
    placeholder?: string;
    disabled?: boolean;
    error?: string;
    rows?: number;
  }>(),
  { disabled: false, rows: 6 },
);

const model = defineModel<string>({ default: "" });
const isFocused = ref(false);

const isFilled = computed(() => model.value.length > 0);

const boxClasses = computed(() => [
  "textarea-box",
  props.error ? "textarea-box--error" : isFilled.value || isFocused.value ? "textarea-box--active" : "textarea-box--default",
  props.disabled && "textarea-box--disabled",
]);
</script>

<template>
  <div class="textarea-wrapper">
    <label class="textarea-label">{{ label }}</label>
    <div :class="boxClasses">
      <textarea
        v-model="model"
        :placeholder="placeholder"
        :disabled="disabled"
        :rows="rows"
        class="textarea-field"
        @focus="isFocused = true"
        @blur="isFocused = false"
      />
    </div>
    <span v-if="error" class="textarea-error">{{ error }}</span>
  </div>
</template>

<style scoped>
.textarea-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  width: 100%;
}

.textarea-label {
  font-family: var(--font);
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--fg);
}

.textarea-box {
  background: #fff;
  padding: 0.75rem 0.875rem;
  width: 100%;
}

.textarea-box--default {
  border: 1px solid var(--border);
}

.textarea-box--active {
  border: 1px solid var(--fg);
}

.textarea-box--error {
  border: 1px solid var(--error);
}

.textarea-box--disabled {
  opacity: 0.45;
  cursor: not-allowed;
  background: var(--surface);
}

.textarea-field {
  border: none;
  outline: none;
  background: transparent;
  font-family: var(--font);
  font-size: 0.75rem;
  font-weight: 400;
  color: var(--fg);
  line-height: 1.6;
  width: 100%;
  resize: vertical;
}

.textarea-field::placeholder {
  color: var(--muted);
}

.textarea-field:disabled {
  cursor: not-allowed;
}

.textarea-error {
  font-family: var(--font);
  font-size: 0.625rem;
  font-weight: 400;
  color: var(--error);
}
</style>
