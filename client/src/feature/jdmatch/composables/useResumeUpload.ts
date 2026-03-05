import { ref, computed, watch } from "vue";
import { z } from "zod";
import type { ResumeSource } from "../types/wizard";

const resumeFileSchema = z.object({
  file: z.any().refine((v): v is File => v instanceof File, "Please upload a resume file"),
});

const resumeUrlSchema = z.object({
  resumeUrl: z
    .string()
    .min(1, "URL is required")
    .url("Please enter a valid URL"),
});

export function useResumeUpload() {
  const activeTab = ref<"file" | "url">("file");
  const file = ref<File | null>(null);
  const resumeUrl = ref("");
  const selectedService = ref("");
  const errors = ref<Record<string, string>>({});

  const serviceDomains: Record<string, string> = {
    "google-drive": "drive.google.com",
    onedrive: "onedrive.live.com",
    dropbox: "dropbox.com",
  };

  const files = computed(() => (file.value ? [file.value] : []));

  const urlPlaceholder = computed(() => {
    const domain = serviceDomains[selectedService.value];
    return domain ? `https://${domain}/...` : "https://drive.google.com/...";
  });

  const urlDomainError = computed(() => {
    if (!selectedService.value || !resumeUrl.value.trim()) return undefined;
    const expectedDomain = serviceDomains[selectedService.value];
    if (!expectedDomain) return undefined;
    try {
      const url = new URL(resumeUrl.value.trim());
      if (!url.hostname.endsWith(expectedDomain)) {
        return `URL must be from ${expectedDomain}`;
      }
    } catch {
      return undefined;
    }
    return undefined;
  });

  const isFileTabDisabled = computed(() => resumeUrl.value.trim().length > 0);
  const isUrlTabDisabled = computed(() => file.value !== null);

  const isValid = computed(() => {
    if (activeTab.value === "file") return file.value !== null;
    return (
      resumeUrl.value.trim().length > 0 &&
      /^https?:\/\/.+/.test(resumeUrl.value) &&
      !urlDomainError.value
    );
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

  function validate(): boolean {
    errors.value = {};

    if (activeTab.value === "file") {
      const result = resumeFileSchema.safeParse({ file: file.value });
      if (!result.success) {
        for (const issue of result.error.issues) {
          const key = String(issue.path[0] ?? "file");
          errors.value[key] = issue.message;
        }
        return false;
      }
      return true;
    }

    const result = resumeUrlSchema.safeParse({
      resumeUrl: resumeUrl.value,
    });
    if (!result.success) {
      for (const issue of result.error.issues) {
        const key = String(issue.path[0] ?? "resumeUrl");
        errors.value[key] = issue.message;
      }
      return false;
    }

    if (urlDomainError.value) {
      errors.value.resumeUrl = urlDomainError.value;
      return false;
    }

    return true;
  }

  watch(activeTab, () => {
    errors.value = {};
  });

  function onFileDrop(files: File[]) {
    file.value = files[0] ?? null;
  }

  function onFilesUpdate(newFiles: File[]) {
    file.value = newFiles[0] ?? null;
  }

  function reset() {
    activeTab.value = "file";
    file.value = null;
    resumeUrl.value = "";
    selectedService.value = "";
    errors.value = {};
  }

  return {
    activeTab,
    file,
    files,
    resumeUrl,
    selectedService,
    urlPlaceholder,
    urlDomainError,
    isFileTabDisabled,
    isUrlTabDisabled,
    isValid,
    errors,
    validate,
    resumeSource,
    fileName,
    fileSize,
    onFileDrop,
    onFilesUpdate,
    reset,
  };
}
