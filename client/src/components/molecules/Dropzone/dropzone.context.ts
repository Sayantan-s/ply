import type { ComputedRef, InjectionKey, Ref } from "vue";

export type DropzoneContext = {
  isDragOver: Ref<boolean>;
  hasFiles: ComputedRef<boolean>;
  acceptedFiles: ComputedRef<File[]>;
  hint: ComputedRef<string>;
  disabled: ComputedRef<boolean>;
  removeFile: (index: number) => void;
  formatSize: (bytes: number) => string;
};

export const DROPZONE_CONTEXT_KEY: InjectionKey<DropzoneContext> =
  Symbol("dropzone");
