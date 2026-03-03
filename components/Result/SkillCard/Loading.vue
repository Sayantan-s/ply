<template>
  <div class="flex gap-1 flex-wrap">
    <div v-for="skill in fallbackSkills" :key="skill" :class="styles" role="button" />
  </div>
</template>

<script setup lang="ts">
interface IProps {
  skills: number;
  variant?: "primary" | "secondary";
}

const { skills, variant = "primary" } = defineProps<IProps>();

const fallbackSkills = computed(() => Array(skills).map((_, index) => index + 1));

const computedVariant = computed(() => ({
  primary: "bg-black text-white",
  secondary: "text-black border-2 border-black bg-transparent",
}));

const styles = ["px-3 py-1 text-sm h-6 w-28", computedVariant.value[variant]];
</script>

<style></style>
