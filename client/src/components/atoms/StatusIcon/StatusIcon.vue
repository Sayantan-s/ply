<script setup lang="ts">
import { computed } from "vue";
import { cva, type VariantProps } from "class-variance-authority";
import { FileX, ZapOff, SearchX } from "lucide-vue-next";

const statusIconVariants = cva("status-icon", {
  variants: {
    variant: {
      error: "status-icon--error",
      warning: "status-icon--warning",
      empty: "status-icon--empty",
    },
  },
  defaultVariants: { variant: "empty" },
});

type StatusIconVariants = VariantProps<typeof statusIconVariants>;

const props = defineProps<{
  variant?: NonNullable<StatusIconVariants["variant"]>;
}>();

const classes = computed(() => statusIconVariants({ variant: props.variant }));

const iconMap = { error: FileX, warning: ZapOff, empty: SearchX } as const;
const iconComponent = computed(() => iconMap[props.variant ?? "empty"]);
</script>

<template>
  <div :class="classes">
    <component :is="iconComponent" class="status-icon__icon" />
  </div>
</template>

<style scoped>
.status-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
}

.status-icon__icon {
  width: 28px;
  height: 28px;
}

.status-icon--error {
  background: var(--error-bg);
}
.status-icon--error .status-icon__icon { color: var(--error); }

.status-icon--warning {
  background: var(--warning-bg);
}
.status-icon--warning .status-icon__icon { color: var(--warning); }

.status-icon--empty {
  background: var(--surface);
}
.status-icon--empty .status-icon__icon { color: #AAAABC; }
</style>
