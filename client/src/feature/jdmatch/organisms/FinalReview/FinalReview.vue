<script setup lang="ts">
import ResumeCard from "../../molecules/ResumeCard/ResumeCard.vue";
import JdCard from "../../molecules/JdCard/JdCard.vue";

defineProps<{
  fileName: string;
  fileSize: string;
  jdPreview: string;
}>();
</script>

<template>
  <div class="final-review">
    <ResumeCard :file-name="fileName" :file-size="fileSize" />
    <JdCard :jd-preview="jdPreview" />
  </div>
</template>

<style scoped>
.final-review {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
}
</style>
