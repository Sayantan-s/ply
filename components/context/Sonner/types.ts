import type { IToastProps } from "~/components/Toast/index.vue";

export type IToastDispatchBody = Pick<IToastProps, "variant" | "title" | "description">;

export interface ToastHandler {
  dispatchToast: (params: IToastDispatchBody) => void;
  removeToast: () => void;
}

export const sonnerHandlerInjectionKey: InjectionKey<ToastHandler> = Symbol("sonner-handlers");
