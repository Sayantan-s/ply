<script setup lang="ts">
import { ToggleGroup, ToggleGroupItem } from "@/components/molecules";

defineProps<{
  modelValue?: string;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: string];
}>();

const services = [
  { value: "google-drive", label: "Google Drive", domain: "drive.google.com" },
  { value: "onedrive", label: "OneDrive", domain: "onedrive.live.com" },
  { value: "dropbox", label: "Dropbox", domain: "dropbox.com" },
] as const;
</script>

<template>
  <ToggleGroup
    :model-value="modelValue"
    @update:model-value="emit('update:modelValue', $event)"
  >
    <ToggleGroupItem
      v-for="service in services"
      :key="service.value"
      :value="service.value"
      :label="service.label"
    />
  </ToggleGroup>
</template>
