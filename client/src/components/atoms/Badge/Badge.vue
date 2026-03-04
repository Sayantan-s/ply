<script setup lang="ts">
import { computed } from "vue";
import { cva, type VariantProps } from "class-variance-authority";
import { Check, X } from "lucide-vue-next";

const badgeVariants = cva("badge", {
  variants: {
    variant: {
      success: "badge--success",
      error: "badge--error",
      neutral: "badge--neutral",
    },
  },
  defaultVariants: { variant: "neutral" },
});

type BadgeVariants = VariantProps<typeof badgeVariants>;

const props = defineProps<{
  variant?: NonNullable<BadgeVariants["variant"]>;
  label: string;
}>();

const classes = computed(() => badgeVariants({ variant: props.variant }));

const iconComponent = computed(() => {
  if (props.variant === "success") return Check;
  if (props.variant === "error") return X;
  return null;
});
</script>

<template>
  <span :class="classes">
    <component v-if="iconComponent" :is="iconComponent" class="badge__icon" />
    <span class="badge__label">{{ label }}</span>
  </span>
</template>

<style scoped>
.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.25rem 0.625rem;
  font-family: var(--font);
  font-size: 0.5625rem;
  font-weight: 600;
}

.badge__icon {
  width: 0.75rem;
  height: 0.75rem;
}

.badge--success {
  background: var(--success-bg);
  color: var(--success);
}

.badge--error {
  background: var(--error-bg);
  color: var(--error);
}

.badge--neutral {
  background: var(--surface);
  color: var(--muted);
}
</style>
