import { ref, computed } from "vue";

export function useJobDescription() {
  const jdText = ref("");
  const jdUrl = ref("");

  const isValid = computed(() => jdText.value.trim().length >= 50 || jdUrl.value.trim().length > 0);

  const jdPreview = computed(() => {
    const text = jdText.value.trim();
    if (text.length <= 150) return text;
    return `${text.slice(0, 150)}...`;
  });

  function reset() {
    jdText.value = "";
    jdUrl.value = "";
  }

  return { jdText, jdUrl, isValid, jdPreview, reset };
}
