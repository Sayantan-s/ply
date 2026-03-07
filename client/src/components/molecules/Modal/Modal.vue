<script setup lang="ts">
import { computed, provide } from "vue";
import {
  DialogRoot,
  DialogPortal,
  DialogOverlay,
  DialogContent,
} from "reka-ui";
import { AnimatePresence, Motion } from "motion-v";
import { cva, type VariantProps } from "class-variance-authority";
import { MODAL_CONTEXT_KEY, type ModalContext } from "./modal.context";

const modalVariants = cva("modal-content", {
  variants: {
    size: {
      sm: "modal-content--sm",
      md: "modal-content--md",
      lg: "modal-content--lg",
    },
  },
  defaultVariants: { size: "md" },
});

type ModalVariants = VariantProps<typeof modalVariants>;

const props = withDefaults(
  defineProps<{
    modelValue: boolean;
    size?: NonNullable<ModalVariants["size"]>;
  }>(),
  { size: "md" },
);

const emit = defineEmits<{
  "update:modelValue": [value: boolean];
}>();

const isOpen = computed({
  get: () => props.modelValue,
  set: (value: boolean) => emit("update:modelValue", value),
});

function close() {
  isOpen.value = false;
}

provide<ModalContext>(MODAL_CONTEXT_KEY, {
  open: computed(() => isOpen.value),
  close,
});
</script>

<template>
  <DialogRoot v-model:open="isOpen">
    <DialogPortal>
      <AnimatePresence>
        <DialogOverlay v-if="isOpen" as-child force-mount>
          <Motion
            as="div"
            class="modal-overlay"
            :initial="{ opacity: 0 }"
            :animate="{ opacity: 1 }"
            :exit="{ opacity: 0 }"
            :transition="{ duration: 0.2 }"
          />
        </DialogOverlay>
      </AnimatePresence>

      <AnimatePresence>
        <DialogContent
          v-if="isOpen"
          as-child
          force-mount
          @escape-key-down="close"
          @pointer-down-outside="close"
        >
          <Motion
            as="div"
            :class="modalVariants({ size: props.size })"
            :initial="{ opacity: 0, scale: 0.95 }"
            :animate="{ opacity: 1, scale: 1 }"
            :exit="{ opacity: 0, scale: 0.95 }"
            :transition="{ type: 'spring', stiffness: 400, damping: 30 }"
          >
            <slot />
          </Motion>
        </DialogContent>
      </AnimatePresence>
    </DialogPortal>
  </DialogRoot>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 50;
}

.modal-content {
  position: fixed;
  top: 50%;
  left: 50%;
  translate: -50% -50%;
  z-index: 51;
  display: flex;
  flex-direction: column;
  width: 90vw;
  background-color: var(--bg);
  color: var(--fg);
  font-family: var(--font);
  border: 1px solid var(--surface);
  border-radius: 0.5rem;
  box-shadow:
    0 20px 25px -5px rgba(0, 0, 0, 0.1),
    0 8px 10px -6px rgba(0, 0, 0, 0.1);
}

.modal-content--sm {
  max-width: 24rem;
}

.modal-content--md {
  max-width: 32rem;
}

.modal-content--lg {
  max-width: 48rem;
}
</style>
