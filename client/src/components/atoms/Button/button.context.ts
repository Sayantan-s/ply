import type { ComputedRef, InjectionKey } from "vue";

export type ButtonContext = {
  loading: ComputedRef<boolean>;
  isDisabled: ComputedRef<boolean>;
};

export const BUTTON_CONTEXT_KEY: InjectionKey<ButtonContext> = Symbol("button");
