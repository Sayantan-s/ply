<script setup lang="ts">
import { TabBar, Tab, TabContent } from "@/components/molecules";
import { File as FileIcon, Link } from "lucide-vue-next";
import { markRaw } from "vue";

const activeTab = defineModel<"file" | "url">({ required: true });

defineProps<{
  fileTabDisabled?: boolean;
  urlTabDisabled?: boolean;
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
          <slot name="file" />
        </div>
      </TabContent>

      <TabContent value="url">
        <div class="resume-upload-form__panel">
          <slot name="url" />
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
