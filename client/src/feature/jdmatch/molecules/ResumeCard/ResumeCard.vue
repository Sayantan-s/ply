<script setup lang="ts">
import { Card, CardHeader, CardBody } from "@/components/molecules";
import { FileText } from "lucide-vue-next";

defineProps<{
  fileName: string;
  fileSize: string;
}>();
</script>

<template>
  <Card>
    <CardHeader :icon="FileText" title="Resume" />
    <CardBody>
      <div class="resume-card__info">
        <span class="resume-card__name">{{ fileName }}</span>
        <span class="resume-card__size">{{ fileSize }}</span>
      </div>
    </CardBody>
  </Card>
</template>

<style scoped>
.resume-card__info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.resume-card__name {
  font-weight: 600;
  color: var(--fg);
}

.resume-card__size {
  color: var(--muted);
}
</style>
