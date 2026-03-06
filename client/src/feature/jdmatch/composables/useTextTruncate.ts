import { ref, computed, type Ref } from "vue";

export function useTextTruncate(lineClamp = 4) {
  const isExpanded = ref(false);
  const textRef: Ref<HTMLElement | null> = ref(null);

  const isClamped = computed(() => {
    const el = textRef.value;
    if (!el) return false;
    return el.scrollHeight > el.clientHeight;
  });

  const showToggle = computed(() => isClamped.value || isExpanded.value);

  function toggle() {
    isExpanded.value = !isExpanded.value;
  }

  return {
    textRef,
    isExpanded,
    showToggle,
    lineClamp,
    toggle,
  };
}
