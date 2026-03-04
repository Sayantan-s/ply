<script setup lang="ts">
import { computed } from "vue";
import { cva, type VariantProps } from "class-variance-authority";

const headingVariants = cva("heading", {
  variants: {
    level: {
      1: "heading--1",
      2: "heading--2",
      3: "heading--3",
      4: "heading--4",
      5: "heading--5",
      6: "heading--6",
    },
  },
  defaultVariants: { level: 1 },
});

type HeadingVariants = VariantProps<typeof headingVariants>;

const props = withDefaults(
  defineProps<{
    level?: NonNullable<HeadingVariants["level"]>;
  }>(),
  { level: 1 },
);

const tag = computed(() => `h${props.level}` as const);
const classes = computed(() => headingVariants({ level: props.level }));
</script>

<template>
  <component :is="tag" :class="classes">
    <slot />
  </component>
</template>

<style scoped>
.heading {
  font-family: var(--font);
  color: var(--fg);
  font-weight: 700;
  margin: 0;
}

/* 1.5rem / 700 / -0.0625rem tracking */
.heading--1 {
  font-size: 1.5rem;
  letter-spacing: -0.0625rem;
}

/* 1.25rem / 700 / -0.0625rem tracking */
.heading--2 {
  font-size: 1.25rem;
  letter-spacing: -0.0625rem;
}

/* 0.8125rem / 700 */
.heading--3 {
  font-size: 0.8125rem;
}

/* 0.75rem / 700 */
.heading--4 {
  font-size: 0.75rem;
}

/* 0.6875rem / 700 */
.heading--5 {
  font-size: 0.6875rem;
}

/* 0.625rem / 700 */
.heading--6 {
  font-size: 0.625rem;
}
</style>
