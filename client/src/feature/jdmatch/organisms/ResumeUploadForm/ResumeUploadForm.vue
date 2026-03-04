<script setup lang="ts">
import { AnimatePresence, Motion } from "motion-v";
import { TabBar, Tab, Dropzone } from "@/components/molecules";
import { Input, Alert } from "@/components/atoms";
import { File as FileIcon, Link } from "lucide-vue-next";
import { markRaw } from "vue";
import CloudServicePicker from "../../molecules/CloudServicePicker/CloudServicePicker.vue";

const activeTab = defineModel<"file" | "url">("activeTab", { required: true });
const resumeUrl = defineModel<string>("resumeUrl", { required: true });

defineProps<{
  disabled?: boolean;
}>();

const emit = defineEmits<{
  fileDrop: [files: File[]];
}>();

const FileIconRaw = markRaw(FileIcon);
const LinkIconRaw = markRaw(Link);
</script>

<template>
  <div class="resume-upload-form">
    <TabBar v-model="activeTab">
      <Tab value="file" :icon="FileIconRaw" label="File Upload" />
      <Tab value="url" :icon="LinkIconRaw" label="Cloud Link" />
    </TabBar>

    <AnimatePresence mode="wait">
      <Motion
        v-if="activeTab === 'file'"
        key="file-panel"
        class="resume-upload-form__panel"
        :initial="{ opacity: 0, y: 8 }"
        :animate="{ opacity: 1, y: 0 }"
        :exit="{ opacity: 0, y: -8 }"
        :transition="{ duration: 0.2 }"
      >
        <Dropzone :disabled="disabled" @drop="emit('fileDrop', $event)" />
      </Motion>

      <Motion
        v-else
        key="url-panel"
        class="resume-upload-form__panel"
        :initial="{ opacity: 0, y: 8 }"
        :animate="{ opacity: 1, y: 0 }"
        :exit="{ opacity: 0, y: -8 }"
        :transition="{ duration: 0.2 }"
      >
        <Input
          v-model="resumeUrl"
          label="Resume URL"
          placeholder="https://drive.google.com/..."
          :icon="LinkIconRaw"
          :disabled="disabled"
        />
        <CloudServicePicker />
        <Alert
          variant="info"
          message="Make sure the file has public or link-shared access enabled."
        />
      </Motion>
    </AnimatePresence>
  </div>
</template>

<style scoped>
.resume-upload-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
}

.resume-upload-form__panel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
