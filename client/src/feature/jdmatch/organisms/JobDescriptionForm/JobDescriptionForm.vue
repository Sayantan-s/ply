<script setup lang="ts">
import { Textarea, Input } from "@/components/atoms";
import { Link } from "lucide-vue-next";
import { markRaw } from "vue";

const jdText = defineModel<string>("jdText", { required: true });
const jdUrl = defineModel<string>("jdUrl", { required: true });

defineProps<{
  jdTextError?: string;
  jdUrlError?: string;
  jdTextDisabled?: boolean;
  jdUrlDisabled?: boolean;
  disabled?: boolean;
}>();

const LinkIcon = markRaw(Link);
</script>

<template>
  <div class="jd-form">
    <Textarea
      v-model="jdText"
      label="Paste Job Description"
      placeholder="Paste the full JD content here..."
      :rows="8"
      :error="jdTextError"
      :disabled="disabled || jdTextDisabled"
    />
    <Input
      v-model="jdUrl"
      label="Job Post URL (optional)"
      placeholder="https://example.com/jobs/..."
      :icon="LinkIcon"
      :error="jdUrlError"
      :disabled="disabled || jdUrlDisabled"
    />
  </div>
</template>

<style scoped>
.jd-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  width: 100%;
}
</style>
