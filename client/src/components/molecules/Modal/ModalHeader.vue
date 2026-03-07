<script setup lang="ts">
import { inject } from "vue";
import { DialogTitle, DialogClose, DialogDescription } from "reka-ui";
import { X } from "lucide-vue-next";
import { MODAL_CONTEXT_KEY, type ModalContext } from "./modal.context";

defineProps<{
  title: string;
  description?: string;
}>();

const context = inject<ModalContext>(MODAL_CONTEXT_KEY);

if (!context) {
  throw new Error("ModalHeader must be used within a Modal component.");
}
</script>

<template>
  <div class="modal-header">
    <div class="modal-header__text">
      <DialogTitle as="h2" class="modal-header__title">
        {{ title }}
      </DialogTitle>
      <DialogDescription
        v-if="description"
        class="modal-header__description"
      >
        {{ description }}
      </DialogDescription>
    </div>
    <DialogClose as-child>
      <button
        class="modal-header__close"
        aria-label="Close dialog"
        @click="context.close"
      >
        <X :size="16" />
      </button>
    </DialogClose>
  </div>
</template>

<style scoped>
.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid var(--surface);
}

.modal-header__text {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 0;
}

.modal-header__title {
  font-family: var(--font);
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--fg);
  margin: 0;
  line-height: 1.4;
}

.modal-header__description {
  font-family: var(--font);
  font-size: 0.75rem;
  color: var(--fg);
  opacity: 0.6;
  margin: 0;
  line-height: 1.4;
}

.modal-header__close {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 1.75rem;
  height: 1.75rem;
  border: none;
  border-radius: 0.25rem;
  background: transparent;
  color: var(--fg);
  opacity: 0.5;
  cursor: pointer;
}

.modal-header__close:hover {
  opacity: 1;
  background-color: var(--surface);
}

.modal-header__close:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
</style>
