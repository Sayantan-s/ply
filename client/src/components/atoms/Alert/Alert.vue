<script setup lang="ts">
import { computed } from "vue";
import { cva, type VariantProps } from "class-variance-authority";
import { CircleX, TriangleAlert, Info, CircleCheck } from "lucide-vue-next";

const alertVariants = cva("alert", {
  variants: {
    variant: {
      error: "alert--error",
      warning: "alert--warning",
      info: "alert--info",
      success: "alert--success",
    },
  },
  defaultVariants: { variant: "info" },
});

type AlertVariants = VariantProps<typeof alertVariants>;

const props = defineProps<{
  variant?: NonNullable<AlertVariants["variant"]>;
  message: string;
}>();

const classes = computed(() => alertVariants({ variant: props.variant }));

const iconMap = { error: CircleX, warning: TriangleAlert, info: Info, success: CircleCheck } as const;
const iconComponent = computed(() => iconMap[props.variant ?? "info"]);

const prefixMap = { error: "err", warning: "warn", info: "info", success: "ok" } as const;
const prefix = computed(() => prefixMap[props.variant ?? "info"]);
</script>

<template>
  <div :class="classes">
    <component :is="iconComponent" class="alert__icon" />
    <p class="alert__message">{{ prefix }}: {{ message }}</p>
  </div>
</template>

<style scoped>
.alert {
  display: flex;
  gap: 8px;
  padding: 12px 14px;
  width: 350px;
  font-family: var(--font);
}

.alert__icon {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
  margin-top: 2px;
}

.alert__message {
  font-size: 10px;
  font-weight: 400;
  line-height: 1.5;
}

.alert--error {
  background: var(--error-bg);
  border: 1px solid var(--error-border);
}
.alert--error .alert__icon { color: var(--error); }
.alert--error .alert__message { color: var(--error-text); }

.alert--warning {
  background: var(--warning-bg);
  border: 1px solid var(--warning-border);
}
.alert--warning .alert__icon { color: var(--warning); }
.alert--warning .alert__message { color: var(--warning-text); }

.alert--info {
  background: var(--info-bg);
  border: 1px solid var(--info-border);
}
.alert--info .alert__icon { color: var(--info); }
.alert--info .alert__message { color: var(--info-text); }

.alert--success {
  background: var(--success-bg);
  border: 1px solid var(--success-border);
}
.alert--success .alert__icon { color: var(--success); }
.alert--success .alert__message { color: var(--success-text); }
</style>
