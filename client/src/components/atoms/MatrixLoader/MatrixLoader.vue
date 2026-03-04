<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import { cva, type VariantProps } from "class-variance-authority";

const CHARS =
  "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789ABCDEF";

const loaderVariants = cva("matrix", {
  variants: {
    variant: {
      text: "matrix--text",
      grid: "matrix--grid",
    },
    size: {
      sm: "matrix--sm",
      md: "matrix--md",
      lg: "matrix--lg",
    },
    tone: {
      inherit: "matrix--inherit",
      accent: "matrix--accent",
      success: "matrix--success",
      muted: "matrix--muted",
    },
  },
  defaultVariants: { variant: "text", size: "sm", tone: "inherit" },
});

export type LoaderVariants = VariantProps<typeof loaderVariants>;

const props = withDefaults(
  defineProps<{
    variant?: NonNullable<LoaderVariants["variant"]>;
    size?: NonNullable<LoaderVariants["size"]>;
    tone?: NonNullable<LoaderVariants["tone"]>;
    cols?: number;
  }>(),
  { variant: "text", size: "sm", tone: "inherit", cols: 5 },
);

const isGrid = computed(() => props.variant === "grid");

const colCount = computed(() => {
  if (isGrid.value) return 3;
  return Math.max(2, Math.min(props.cols, 12));
});

const totalCells = computed(() => (isGrid.value ? 9 : colCount.value));

function randomChar() {
  return CHARS[Math.floor(Math.random() * CHARS.length)];
}

function randomOpacity() {
  return 0.25 + Math.random() * 0.75;
}

function generateCells() {
  return Array.from({ length: totalCells.value }, () => ({
    char: randomChar(),
    opacity: randomOpacity(),
  }));
}

const cells = ref(generateCells());

let interval: ReturnType<typeof setInterval> | undefined;

onMounted(() => {
  interval = setInterval(
    () => {
      const idx = Math.floor(Math.random() * totalCells.value);
      cells.value[idx] = { char: randomChar(), opacity: randomOpacity() };
    },
    isGrid.value ? 150 : 100,
  );
});

onUnmounted(() => {
  clearInterval(interval);
});

const classes = computed(() =>
  loaderVariants({
    variant: props.variant,
    size: props.size,
    tone: props.tone,
  }),
);
</script>

<template>
  <span :class="classes" role="status" aria-label="Loading">
    <!-- Grid variant: 3x3 rounded squares -->
    <template v-if="isGrid">
      <span
        v-for="(cell, i) in cells"
        :key="i"
        class="matrix__dot"
        :style="{ opacity: cell.opacity }"
      />
    </template>

    <!-- Text variant: cycling characters -->
    <template v-else>
      <span
        v-for="(cell, i) in cells"
        :key="i"
        :class="['matrix__cell', cell.opacity < 0.5 && 'matrix__cell--dim']"
        >{{ cell.char }}</span
      >
    </template>
  </span>
</template>

<style scoped>
.matrix {
  display: inline-flex;
  vertical-align: middle;
  overflow: hidden;
}

/* ── Text variant ── */
.matrix--text {
  gap: 0.125em;
  font-family: var(--font);
  font-weight: 600;
  line-height: 1;
  letter-spacing: 0.05em;
}

/* ── Grid variant ── */
.matrix--grid {
  display: inline-grid;
  grid-template-columns: repeat(3, 1fr);
}

.matrix--grid.matrix--sm {
  gap: 0.1875rem;
}

.matrix--grid.matrix--md {
  gap: 0.25rem;
}

.matrix--grid.matrix--lg {
  gap: 0.3125rem;
}

/* ── Sizes ── */
.matrix--grid.matrix--sm {
  font-size: 0.25rem;
}

.matrix--grid.matrix--md {
  font-size: 0.4rem;
}

.matrix--grid.matrix--lg {
  font-size: 0.6rem;
}

.matrix--text.matrix--sm {
  font-size: 0.625rem;
}

.matrix--text.matrix--md {
  font-size: 0.8125rem;
}

.matrix--text.matrix--lg {
  font-size: 1.125rem;
}

/* ── Tones ── */
.matrix--inherit {
  color: currentColor;
}

.matrix--accent {
  color: var(--accent);
}

.matrix--success {
  color: var(--success);
}

.matrix--muted {
  color: var(--muted);
}

/* ── Text cells ── */
.matrix__cell {
  display: inline-block;
  width: 1em;
  text-align: center;
  opacity: 1;
  transition: opacity 0.15s ease;
}

.matrix__cell--dim {
  opacity: 0.3;
}

/* ── Grid dots ── */
.matrix__dot {
  width: 1em;
  height: 1em;
  border-radius: 0.1875em;
  background: currentColor;
  transition: opacity 0.3s ease;
}
</style>
