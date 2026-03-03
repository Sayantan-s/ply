<template>
  <div class="border-b-2 border-black">
    <div class="flex items-center border-2 border-black gap-4 mb-6">
      <div :class="styles">{{ score }} <sup class="text-xs text-black/60">/ 100</sup></div>
      <div>
        <strong>Feedback</strong>
        <p class="text-sm" v-html="computedMeta?.feedback" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface IProps {
  score: number;
  resumeName: string;
}

const { score, resumeName } = defineProps<IProps>();

const computedMeta = computed(() => {
  if (score < 40) {
    return {
      feedback: `Not recommended – significant gaps in both skills and fit for the role.`,
      style: "bg-rose-600",
    };
  } else if (score >= 40 && score < 70) {
    return {
      feedback: `Not recommended – some relevant qualities, but key requirements unmet.`,
      style: "bg-yellow-600",
    };
  } else if (score >= 70 && score < 90) {
    return {
      feedback: `Recommended – meets expectations with room to grow. <br /> You can apply using
      <span class="text-purple-700">${resumeName}</span>`,
      style: "bg-green-600",
    };
  } else if (score >= 90) {
    return {
      feedback: `Your are highly recommended for this job! <br />
      Do apply to this job using <span class="text-purple-700">${resumeName}</span>`,
      style: "bg-emerald-600",
    };
  } else {
    return null;
  }
});

const styles = computed(() => [
  "w-24 aspect-square border-r-2 border-black text-4xl flex items-center justify-center",
  computedMeta.value?.style,
]);
</script>
