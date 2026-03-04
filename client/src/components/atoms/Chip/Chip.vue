<script setup lang="ts">
import { computed, type Component } from "vue";
import { cva, type VariantProps } from "class-variance-authority";

const chipVariants = cva("chip", {
  variants: {
    variant: {
      active: "chip--active",
      default: "chip--default",
    },
  },
  defaultVariants: { variant: "default" },
});

type ChipVariants = VariantProps<typeof chipVariants>;

const props = defineProps<{
  variant?: NonNullable<ChipVariants["variant"]>;
  icon?: Component;
  label: string;
}>();

const classes = computed(() => chipVariants({ variant: props.variant }));
</script>

<template>
  <span :class="classes">
    <component v-if="icon" :is="icon" class="chip__icon" />
    <span class="chip__label">{{ label }}</span>
  </span>
</template>

<style scoped>
.chip {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  padding: 0.5rem 0.875rem;
  font-family: var(--font);
  font-size: 0.625rem;
  font-weight: 600;
}

.chip__icon {
  width: 0.875rem;
  height: 0.875rem;
}

.chip--active {
  background: var(--fg);
  color: #fff;
}

.chip--default {
  background: transparent;
  color: var(--muted);
  border: 1px solid var(--border);
}
</style>
