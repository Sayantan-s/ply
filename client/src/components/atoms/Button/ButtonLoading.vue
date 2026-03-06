<script setup lang="ts">
import { inject } from "vue";
import MatrixLoader from "@/components/atoms/MatrixLoader/MatrixLoader.vue";
import type { LoaderVariants } from "@/components/atoms/MatrixLoader/MatrixLoader.vue";
import { BUTTON_CONTEXT_KEY } from "./button.context";

const props = withDefaults(
  defineProps<{
    variant?: NonNullable<LoaderVariants["variant"]>;
    size?: NonNullable<LoaderVariants["size"]>;
    tone?: NonNullable<LoaderVariants["tone"]>;
    cols?: number;
  }>(),
  { variant: "text", size: "sm", tone: "inherit", cols: 3 },
);

const ctx = inject(BUTTON_CONTEXT_KEY)!;
</script>

<template>
  <template v-if="ctx.loading.value">
    <MatrixLoader :variant="variant" :size="size" :tone="tone" :cols="cols" />
    <slot />
  </template>
</template>
