<script setup lang="ts">
import { Card, CardHeader, CardBody } from "@/components/molecules";
import { FileText } from "lucide-vue-next";

defineProps<{
  jdPreview: string;
}>();
</script>

<template>
  <Card>
    <CardHeader :icon="FileText" title="Job Description" />
    <CardBody>{{ jdPreview }}</CardBody>
  </Card>
</template>
