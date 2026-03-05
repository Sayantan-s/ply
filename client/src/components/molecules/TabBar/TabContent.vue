<script setup lang="ts">
import { TabsContent } from "reka-ui";

defineProps<{
  value: string;
  forceMount?: boolean;
}>();
</script>

<template>
  <TabsContent :value="value" :force-mount="forceMount">
    <slot />
  </TabsContent>
</template>
