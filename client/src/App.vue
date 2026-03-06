<script setup lang="ts">
import { MotionConfig } from "motion-v";
import { RouterView } from "vue-router";
</script>

<template>
  <MotionConfig reduce-motion="user">
    <RouterView />
  </MotionConfig>
</template>
