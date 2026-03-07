<script setup lang="ts">
import { useRouter } from "vue-router";
import { useJdMatchReport } from "../composables/useJdMatchReport";
import StepLayout from "../templates/StepLayout.vue";
import { WizardNavBarReport } from "../molecules/WizardNavBar";
import MatchReport from "../organisms/MatchReport/MatchReport.vue";
import MatchReportSkeleton from "../organisms/MatchReport/MatchReportSkeleton.vue";
import ErrorState from "../organisms/ErrorState/ErrorState.vue";

const props = defineProps<{
  jdMatchId: string;
}>();

const router = useRouter();
const { analysis, isLoading, isError } = useJdMatchReport(props.jdMatchId);

function handleNewMatch() {
  router.push({ name: "home" });
}
</script>

<template>
  <StepLayout no-card page>
    <template #nav>
      <WizardNavBarReport @back="handleNewMatch" />
    </template>

    <MatchReportSkeleton v-if="isLoading" />

    <ErrorState
      v-else-if="isError"
      variant="analysis"
      error-message="Failed to load report"
      @retry="() => router.go(0)"
      @go-back="handleNewMatch"
    />

    <MatchReport
      v-else-if="analysis"
      :analysis="analysis"
      @new-match="handleNewMatch"
      @download="() => {}"
    />
  </StepLayout>
</template>
