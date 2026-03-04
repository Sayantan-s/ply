<script setup lang="ts">
import { computed } from "vue";
import { cva, type VariantProps } from "class-variance-authority";

const textVariants = cva("text", {
  variants: {
    variant: {
      body: "text--body",
      label: "text--label",
      comment: "text--comment",
      caption: "text--caption",
      muted: "text--muted",
    },
  },
  defaultVariants: { variant: "body" },
});

type TextVariants = VariantProps<typeof textVariants>;

const props = withDefaults(
  defineProps<{
    as?: string;
    variant?: NonNullable<TextVariants["variant"]>;
  }>(),
  { as: "p", variant: "body" },
);

const classes = computed(() => textVariants({ variant: props.variant }));
</script>

<template>
  <component :is="as" :class="classes">
    <slot />
  </component>
</template>

<style scoped>
.text {
  font-family: var(--font);
  margin: 0;
}

/* 0.75rem / 400 / muted */
.text--body {
  font-size: 0.75rem;
  font-weight: 400;
  color: #777788;
  line-height: 1.5;
}

/* 0.6875rem / 600 / foreground */
.text--label {
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--fg);
}

/* 0.6875rem / 400 / accent (code comment style) */
.text--comment {
  font-size: 0.6875rem;
  font-weight: 400;
  color: var(--accent);
}

/* 0.625rem / 400 / muted-fg */
.text--caption {
  font-size: 0.625rem;
  font-weight: 400;
  color: var(--muted);
}

/* 0.5625rem / 600 / muted — for badges, units */
.text--muted {
  font-size: 0.5625rem;
  font-weight: 600;
  color: var(--muted);
}
</style>
