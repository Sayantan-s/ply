import { ref, computed } from "vue";
import type { ResumeSource } from "../types/wizard";

export function useResumeUpload() {
  const activeTab = ref<"file" | "url">("file");
  const file = ref<File | null>(null);
  const resumeUrl = ref("");

  const isValid = computed(() => {
    if (activeTab.value === "file") return file.value !== null;
    return resumeUrl.value.trim().length > 0 && /^https?:\/\/.+/.test(resumeUrl.value);
  });

  const resumeSource = computed<ResumeSource | null>(() => {
    if (activeTab.value === "file" && file.value) {
      return { type: "file", file: file.value };
    }
    if (activeTab.value === "url" && resumeUrl.value.trim()) {
      return { type: "url", url: resumeUrl.value.trim() };
    }
    return null;
  });

  const fileName = computed(() => {
    if (file.value) return file.value.name;
    if (resumeUrl.value.trim()) return resumeUrl.value.trim();
    return "";
  });

  const fileSize = computed(() => {
    if (!file.value) return "";
    const bytes = file.value.size;
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  });

  function onFileDrop(files: File[]) {
    file.value = files[0] ?? null;
  }

  function reset() {
    activeTab.value = "file";
    file.value = null;
    resumeUrl.value = "";
  }

  return {
    activeTab,
    file,
    resumeUrl,
    isValid,
    resumeSource,
    fileName,
    fileSize,
    onFileDrop,
    reset,
  };
}
