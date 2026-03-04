<script setup lang="ts">
import { computed, type Component } from "vue";
import { cva, type VariantProps } from "class-variance-authority";
import { Motion } from "motion-v";

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

const props = defineProps<{
  variant?: NonNullable<ButtonVariants["variant"]>;
  icon?: Component;
  label: string;
}>();

const classes = computed(() => buttonVariants({ variant: props.variant }));
</script>

<template>
  <Motion
    as="button"
    :class="classes"
    :hover="{ scale: 1.02 }"
    :press="{ scale: 0.97 }"
    :transition="{ type: 'spring', stiffness: 400, damping: 17 }"
  >
    <component v-if="icon" :is="icon" class="button__icon" />
    <span class="button__label">{{ label }}</span>
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

.button__icon {
  width: 1rem;
  height: 1rem;
}

.button--outline .button__icon {
  width: 0.875rem;
  height: 0.875rem;
}
</style>
