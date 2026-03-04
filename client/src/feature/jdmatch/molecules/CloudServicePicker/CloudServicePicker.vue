<script setup lang="ts">
import { Chip } from "@/components/atoms";
</script>

<template>
  <div class="cloud-service-picker">
    <Chip label="Google Drive" />
    <Chip label="OneDrive" />
    <Chip label="Dropbox" />
  </div>
</template>

<style scoped>
.cloud-service-picker {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
</style>
