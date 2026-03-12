import { ref, computed } from "vue";
import { z } from "zod";

const jdSchema = z
  .object({
    jdText: z.string(),
    jdUrl: z.string(),
  })
  .refine(
    (data) =>
      data.jdText.trim().length >= 50 ||
      (data.jdUrl.trim().length > 0 && /^https?:\/\/.+/.test(data.jdUrl)),
    {
      message:
        "Provide a job description (min 50 chars) or a valid job post URL",
    },
  );

const jdUrlFormatSchema = z.string().url("Please enter a valid URL");

export function useJobDescription() {
  const jdText = ref("");
  const jdUrl = ref("");
  const errors = ref<Record<string, string>>({});

  const isValid = computed(
    () => jdText.value.trim().length >= 50 || jdUrl.value.trim().length > 0,
  );

  const isJdTextDisabled = computed(() => jdUrl.value.trim().length > 0);
  const isJdUrlDisabled = computed(() => jdText.value.trim().length > 0);

  const jdPreview = computed(() => {
    const text = jdText.value.trim() || jdUrl.value.trim();
    if (text.length <= 150) return text;
    return `${text.slice(0, 150)}...`;
  });

  function validate(): boolean {
    errors.value = {};

    const text = jdText.value.trim();
    const url = jdUrl.value.trim();

    if (text.length > 0 && text.length < 50) {
      errors.value.jdText = "Job description must be at least 50 characters";
      return false;
    }

    if (url.length > 0) {
      const result = jdUrlFormatSchema.safeParse(url);
      if (!result.success) {
        errors.value.jdUrl = result.error.issues[0].message;
        return false;
      }
    }

    const overallResult = jdSchema.safeParse({
      jdText: jdText.value,
      jdUrl: jdUrl.value,
    });
    if (!overallResult.success) {
      errors.value.jdText = overallResult.error.issues[0].message;
      return false;
    }

    return true;
  }

  function reset() {
    jdText.value = "";
    jdUrl.value = "";
    errors.value = {};
  }

  return {
    jdText,
    jdUrl,
    isValid,
    isJdTextDisabled,
    isJdUrlDisabled,
    errors,
    validate,
    jdPreview,
    reset,
  };
}
