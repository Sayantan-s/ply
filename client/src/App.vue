<script setup lang="ts">
import { MotionConfig } from "motion-v";
import { JdMatchPage } from "@/feature/jdmatch";
</script>

<template>
  <MotionConfig reduce-motion="user">
    <JdMatchPage />
  </MotionConfig>
</template>
