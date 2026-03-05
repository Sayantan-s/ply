<script setup lang="ts">
import { TabBar, Tab, TabContent, Dropzone } from "@/components/molecules";
import { Input, Alert } from "@/components/atoms";
import { File as FileIcon, Link } from "lucide-vue-next";
import { markRaw } from "vue";
import CloudServicePicker from "../../molecules/CloudServicePicker/CloudServicePicker.vue";

const activeTab = defineModel<"file" | "url">("activeTab", { required: true });
const resumeUrl = defineModel<string>("resumeUrl", { required: true });

defineProps<{
  files?: File[];
  disabled?: boolean;
  fileTabDisabled?: boolean;
  urlTabDisabled?: boolean;
  fileError?: string;
  urlError?: string;
  selectedService?: string;
  urlPlaceholder?: string;
}>();

const emit = defineEmits<{
  "update:files": [files: File[]];
  "update:selectedService": [value: string];
}>();

const FileIconRaw = markRaw(FileIcon);
const LinkIconRaw = markRaw(Link);
</script>

<template>
  <div class="resume-upload-form">
    <TabBar v-model="activeTab">
      <template #triggers>
        <Tab value="file" :icon="FileIconRaw" label="File Upload" :disabled="fileTabDisabled" />
        <Tab value="url" :icon="LinkIconRaw" label="Cloud Link" :disabled="urlTabDisabled" />
      </template>

      <TabContent value="file">
        <div class="resume-upload-form__panel">
          <Dropzone
            :model-value="files"
            :disabled="disabled"
            @update:model-value="emit('update:files', $event)"
          />
          <span v-if="fileError" class="resume-upload-form__error">{{ fileError }}</span>
        </div>
      </TabContent>

      <TabContent value="url">
        <div class="resume-upload-form__panel">
          <Input
            v-model="resumeUrl"
            label="Resume URL"
            :placeholder="urlPlaceholder ?? 'https://drive.google.com/...'"
            :icon="LinkIconRaw"
            :disabled="disabled"
            :error="urlError"
          />
          <CloudServicePicker
            :model-value="selectedService"
            @update:model-value="emit('update:selectedService', $event)"
          />
          <Alert
            variant="info"
            message="Make sure the file has public or link-shared access enabled."
          />
        </div>
      </TabContent>
    </TabBar>
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
  padding-top: 1rem;
  min-height: 13.5rem;
}

.resume-upload-form__error {
  font-family: var(--font);
  font-size: 0.625rem;
  font-weight: 400;
  color: var(--error);
}
</style>
