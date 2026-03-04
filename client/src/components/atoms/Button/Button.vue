<script setup lang="ts">
import { computed } from "vue";
import { cva, type VariantProps } from "class-variance-authority";
import { Motion } from "motion-v";
import { LoaderCircle } from "lucide-vue-next";

const buttonVariants = cva("button", {
  variants: {
    variant: {
      primary: "button--primary",
      accent: "button--accent",
      outline: "button--outline",
      ghost: "button--ghost",
    },
  },
  defaultVariants: { variant: "primary" },
});

type ButtonVariants = VariantProps<typeof buttonVariants>;

const props = withDefaults(
  defineProps<{
    variant?: NonNullable<ButtonVariants["variant"]>;
    disabled?: boolean;
    loading?: boolean;
    fluid?: boolean;
  }>(),
  { variant: "primary", disabled: false, loading: false, fluid: false },
);

const isDisabled = computed(() => props.disabled || props.loading);

const classes = computed(() => [
  buttonVariants({ variant: props.variant }),
  props.fluid && "button--fluid",
  isDisabled.value && "button--disabled",
]);
</script>

<template>
  <Motion
    as="button"
    :class="classes"
    :disabled="isDisabled"
    :hover="isDisabled ? undefined : { scale: 1.02 }"
    :press="isDisabled ? undefined : { scale: 0.97 }"
    :transition="{ type: 'spring', stiffness: 400, damping: 17 }"
  >
    <template v-if="loading">
      <LoaderCircle class="button__spinner" />
      <slot />
    </template>
    <slot v-else />
  </Motion>
</template>

<style scoped>
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-family: var(--font);
  font-weight: 600;
  border: none;
  cursor: pointer;
  outline: none;
}

.button--fluid {
  width: 100%;
}

.button--disabled {
  cursor: not-allowed;
  opacity: 0.45;
}

.button--primary {
  height: 3rem;
  padding: 0 1.5rem;
  background: var(--fg);
  color: #fff;
  font-size: 0.8125rem;
}

.button--accent {
  height: 3rem;
  padding: 0 1.5rem;
  background: var(--accent);
  color: #fff;
  font-size: 0.8125rem;
}

.button--outline {
  height: 2.75rem;
  padding: 0 1.25rem;
  background: transparent;
  color: var(--fg);
  font-size: 0.75rem;
  border: 1px solid var(--border);
}

.button--ghost {
  height: 2.5rem;
  padding: 0 1rem;
  background: transparent;
  color: var(--muted);
  font-size: 0.75rem;
  font-weight: 500;
}

.button__spinner {
  width: 1rem;
  height: 1rem;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
