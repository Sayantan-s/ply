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
  gap: 8px;
  font-family: var(--font);
  font-weight: 600;
  border: none;
  cursor: pointer;
  outline: none;
}

.button--primary {
  height: 48px;
  padding: 0 24px;
  background: var(--fg);
  color: #fff;
  font-size: 13px;
}

.button--accent {
  height: 48px;
  padding: 0 24px;
  background: var(--accent);
  color: #fff;
  font-size: 13px;
}

.button--outline {
  height: 44px;
  padding: 0 20px;
  background: transparent;
  color: var(--fg);
  font-size: 12px;
  border: 1px solid var(--border);
}

.button--ghost {
  height: 40px;
  padding: 0 16px;
  background: transparent;
  color: var(--muted);
  font-size: 12px;
  font-weight: 500;
}

.button__icon {
  width: 16px;
  height: 16px;
}

.button--outline .button__icon {
  width: 14px;
  height: 14px;
}
</style>
