import type { InjectionKey, Ref } from "vue";

export interface ModalContext {
  open: Ref<boolean>;
  close: () => void;
}

export const MODAL_CONTEXT_KEY: InjectionKey<ModalContext> =
  Symbol("modal-context");
