<script setup lang="ts">
import { computed, type Component } from "vue";
import { cva, type VariantProps } from "class-variance-authority";

const inputVariants = cva("input-box", {
  variants: {
    filled: {
      true: "input-box--filled",
      false: "input-box--default",
    },
  },
  defaultVariants: { filled: false },
});

type InputVariants = VariantProps<typeof inputVariants>;

const props = defineProps<{
  label: string;
  placeholder?: string;
  icon?: Component;
}>();

const model = defineModel<string>({ default: "" });

const isFilled = computed(() => model.value.length > 0);
const boxClasses = computed(() => inputVariants({ filled: isFilled.value }));
</script>

<template>
  <div class="input-wrapper">
    <label class="input-label">{{ label }}</label>
    <div :class="boxClasses">
      <component v-if="icon" :is="icon" class="input-icon" />
      <input
        v-model="model"
        :placeholder="placeholder"
        class="input-field"
      />
    </div>
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

.input-box--filled {
  border: 1px solid var(--fg);
}

.input-icon {
  width: 0.875rem;
  height: 0.875rem;
  flex-shrink: 0;
}

.input-box--default .input-icon {
  color: var(--muted);
}

.input-box--filled .input-icon {
  color: var(--fg);
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
</style>
