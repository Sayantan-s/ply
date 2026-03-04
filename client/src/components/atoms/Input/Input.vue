<script setup lang="ts">
import { computed, ref, type Component } from "vue";

const props = withDefaults(
  defineProps<{
    label: string;
    placeholder?: string;
    icon?: Component;
    disabled?: boolean;
    error?: string;
  }>(),
  { disabled: false },
);

const model = defineModel<string>({ default: "" });
const isFocused = ref(false);

const isFilled = computed(() => model.value.length > 0);

const boxClasses = computed(() => [
  "input-box",
  props.error ? "input-box--error" : isFilled.value || isFocused.value ? "input-box--active" : "input-box--default",
  props.disabled && "input-box--disabled",
]);
</script>

<template>
  <div class="input-wrapper">
    <label class="input-label">{{ label }}</label>
    <div :class="boxClasses">
      <component v-if="icon" :is="icon" class="input-icon" />
      <input
        v-model="model"
        :placeholder="placeholder"
        :disabled="disabled"
        class="input-field"
        @focus="isFocused = true"
        @blur="isFocused = false"
      />
    </div>
    <span v-if="error" class="input-error">{{ error }}</span>
  </div>
</template>

<style scoped>
.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.375rem;
  width: 100%;
}

.input-label {
  font-family: var(--font);
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--fg);
}

.input-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  height: 2.75rem;
  padding: 0 0.875rem;
  background: #fff;
  width: 100%;
}

.input-box--default {
  border: 1px solid var(--border);
}

.input-box--active {
  border: 1px solid var(--fg);
}

.input-box--error {
  border: 1px solid var(--error);
}

.input-box--disabled {
  opacity: 0.45;
  cursor: not-allowed;
  background: var(--surface);
}

.input-icon {
  width: 0.875rem;
  height: 0.875rem;
  flex-shrink: 0;
}

.input-box--default .input-icon {
  color: var(--muted);
}

.input-box--active .input-icon {
  color: var(--fg);
}

.input-box--error .input-icon {
  color: var(--error);
}

.input-field {
  border: none;
  outline: none;
  background: transparent;
  font-family: var(--font);
  font-size: 0.75rem;
  font-weight: 400;
  color: var(--fg);
  width: 100%;
}

.input-field::placeholder {
  color: var(--muted);
}

.input-field:disabled {
  cursor: not-allowed;
}

.input-error {
  font-family: var(--font);
  font-size: 0.625rem;
  font-weight: 400;
  color: var(--error);
}
</style>
