import { ref, readonly } from "vue";
import type { CreateJdMatchPayload, ResumeUploadData } from "../types/api";
import { createJdMatch } from "../api/jdmatch";

export function useCreateJdMatch() {
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  async function execute(payload: CreateJdMatchPayload): Promise<ResumeUploadData | null> {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await createJdMatch(payload);
      if (!response.success || !response.data) {
        error.value = response.error?.join(", ") ?? "Upload failed";
        return null;
      }
      return response.data;
    } catch (e) {
      error.value = e instanceof Error ? e.message : "Upload failed";
      return null;
    } finally {
      isLoading.value = false;
    }
  }

  return { execute, isLoading: readonly(isLoading), error: readonly(error) };
}
