<script setup lang="ts">
import { computed, ref, watch, markRaw } from "vue";
import { AnimatePresence, Motion } from "motion-v";
import { ArrowRight, ArrowLeft, Sparkles } from "lucide-vue-next";
import { Button } from "@/components/atoms";
import { WizardStep } from "../types/wizard";
import { useJdMatchPage } from "../composables/useJdMatchPage";
import StepLayout from "../templates/StepLayout.vue";
import StepHeadline from "../molecules/StepHeadline/StepHeadline.vue";
import ResumeUploadForm from "../organisms/ResumeUploadForm/ResumeUploadForm.vue";
import JobDescriptionForm from "../organisms/JobDescriptionForm/JobDescriptionForm.vue";
import FinalReview from "../organisms/FinalReview/FinalReview.vue";
import AnalysisLoading from "../organisms/AnalysisLoading/AnalysisLoading.vue";
import MatchReport from "../organisms/MatchReport/MatchReport.vue";
import ErrorState from "../organisms/ErrorState/ErrorState.vue";
import EmptyState from "../organisms/EmptyState/EmptyState.vue";

const {
  wizard,
  resumeUpload,
  jobDescription,
  createMutation,
  analyzeMutation,
  handleSubmitAndAnalyze,
  handleStartOver,
} = useJdMatchPage();

const ArrowRightIcon = markRaw(ArrowRight);
const ArrowLeftIcon = markRaw(ArrowLeft);
const SparklesIcon = markRaw(Sparkles);

const isSubmitting = computed(
  () => createMutation.isLoading.value || analyzeMutation.isStreaming.value,
);

function handleNextFromResume() {
  if (resumeUpload.validate()) {
    wizard.nextFromResume();
  }
}

function handleNextFromJd() {
  if (jobDescription.validate()) {
    wizard.nextFromJd();
  }
}

const navVariant = computed(() => {
  if (wizard.step.value === WizardStep.Report) return "report" as const;
  if (wizard.step.value === WizardStep.EmptyResult) return "empty" as const;
  return "wizard" as const;
});

const activeNavStep = computed(() => {
  const map: Partial<Record<WizardStep, number>> = {
    [WizardStep.ResumeUpload]: 1,
    [WizardStep.JobDescription]: 2,
    [WizardStep.FinalReview]: 3,
    [WizardStep.Analyzing]: 3,
    [WizardStep.UploadError]: 1,
    [WizardStep.AnalysisError]: 3,
  };
  return map[wizard.step.value];
});

const isErrorOrEmpty = computed(() =>
  [WizardStep.UploadError, WizardStep.AnalysisError, WizardStep.EmptyResult].includes(
    wizard.step.value,
  ),
);

const cardWidth = computed(() => (isErrorOrEmpty.value ? 480 : undefined));
const noCard = computed(() => wizard.step.value === WizardStep.Report);

const stepOrder: Record<WizardStep, number> = {
  [WizardStep.ResumeUpload]: 1,
  [WizardStep.UploadError]: 1,
  [WizardStep.JobDescription]: 2,
  [WizardStep.FinalReview]: 3,
  [WizardStep.Analyzing]: 4,
  [WizardStep.AnalysisError]: 4,
  [WizardStep.Report]: 5,
  [WizardStep.EmptyResult]: 5,
};

const direction = ref(1);

watch(
  () => wizard.step.value,
  (next, prev) => {
    direction.value = stepOrder[next] >= stepOrder[prev] ? 1 : -1;
  },
);

const transition = computed(() => ({
  initial: { opacity: 0, x: 24 * direction.value },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: -24 * direction.value },
  transition: { duration: 0.25 },
}));
</script>

<template>
  <StepLayout
    :nav-variant="navVariant"
    :active-step="activeNavStep"
    :card-width="cardWidth"
    :no-card="noCard"
    @nav-back="handleStartOver"
  >
    <AnimatePresence mode="wait">
      <!-- Step 1: Resume Upload -->
      <Motion
        v-if="wizard.step.value === WizardStep.ResumeUpload"
        key="step-1"
        class="step-content"
        v-bind="transition"
      >
        <StepHeadline
          step-comment="// step_01"
          title="Upload Resume"
          subtitle="We'll analyze it against your target job description."
        />
        <ResumeUploadForm
          v-model:active-tab="resumeUpload.activeTab.value"
          v-model:resume-url="resumeUpload.resumeUrl.value"
          :files="resumeUpload.files.value"
          :file-tab-disabled="resumeUpload.isFileTabDisabled.value"
          :url-tab-disabled="resumeUpload.isUrlTabDisabled.value"
          :selected-service="resumeUpload.selectedService.value"
          :url-placeholder="resumeUpload.urlPlaceholder.value"
          :file-error="resumeUpload.errors.value.file"
          :url-error="resumeUpload.errors.value.resumeUrl ?? resumeUpload.urlDomainError.value"
          @update:files="resumeUpload.onFilesUpdate"
          @update:selected-service="resumeUpload.selectedService.value = $event"
        />
        <Button
          variant="primary"
          fluid
          :disabled="!resumeUpload.isValid.value"
          @click="handleNextFromResume()"
        >
          next: job_description
          <component :is="ArrowRightIcon" :size="18" />
        </Button>
      </Motion>

      <!-- Step 2: Job Description -->
      <Motion
        v-else-if="wizard.step.value === WizardStep.JobDescription"
        key="step-2"
        class="step-content"
        v-bind="transition"
      >
        <StepHeadline
          step-comment="// step_02"
          title="Job Details"
          subtitle="Paste the job description or provide the job post URL."
        />
        <JobDescriptionForm
          v-model:jd-text="jobDescription.jdText.value"
          v-model:jd-url="jobDescription.jdUrl.value"
          :jd-text-error="jobDescription.errors.value.jdText"
          :jd-url-error="jobDescription.errors.value.jdUrl"
          :jd-text-disabled="jobDescription.isJdTextDisabled.value"
          :jd-url-disabled="jobDescription.isJdUrlDisabled.value"
        />
        <div class="step-footer-row">
          <Button variant="outline" fluid @click="wizard.backToResume()">
            <component :is="ArrowLeftIcon" :size="14" />
            back
          </Button>
          <Button
            variant="primary"
            fluid
            :disabled="!jobDescription.isValid.value"
            @click="handleNextFromJd()"
          >
            next: review
            <component :is="ArrowRightIcon" :size="18" />
          </Button>
        </div>
      </Motion>

      <!-- Step 3: Final Review -->
      <Motion
        v-else-if="wizard.step.value === WizardStep.FinalReview"
        key="step-3"
        class="step-content"
        v-bind="transition"
      >
        <StepHeadline
          step-comment="// step_03"
          title="Final Review"
          subtitle="Confirm your inputs before running the analysis."
        />
        <FinalReview
          :file-name="resumeUpload.fileName.value"
          :file-size="resumeUpload.fileSize.value"
          :jd-preview="jobDescription.jdPreview.value"
        />
        <div class="step-footer-col">
          <Button
            variant="accent"
            fluid
            :loading="isSubmitting"
            :disabled="isSubmitting"
            @click="handleSubmitAndAnalyze"
          >
            <component :is="SparklesIcon" :size="18" />
            Run Match Report
          </Button>
          <Button variant="ghost" fluid @click="wizard.backToJd()">
            go_back
          </Button>
        </div>
      </Motion>

      <!-- Analyzing -->
      <Motion
        v-else-if="wizard.step.value === WizardStep.Analyzing"
        key="analyzing"
        class="step-content"
        v-bind="transition"
      >
        <StepHeadline
          step-comment="// analyzing"
          title="Running Analysis"
          subtitle="Sit tight while we crunch the numbers."
        />
        <AnalysisLoading
          :status-history="analyzeMutation.statusHistory.value"
          :current-status="analyzeMutation.currentStatus.value"
        />
      </Motion>

      <!-- Match Report -->
      <Motion
        v-else-if="wizard.step.value === WizardStep.Report && wizard.analysis.value"
        key="report"
        v-bind="transition"
      >
        <MatchReport
          :analysis="wizard.analysis.value"
          @new-match="handleStartOver"
          @download="() => {}"
        />
      </Motion>

      <!-- Upload Error -->
      <Motion
        v-else-if="wizard.step.value === WizardStep.UploadError"
        key="upload-error"
        v-bind="transition"
      >
        <ErrorState
          variant="upload"
          :error-message="wizard.error.value ?? undefined"
          @retry="wizard.backToResume()"
          @go-back="wizard.backToResume()"
        />
      </Motion>

      <!-- Analysis Error -->
      <Motion
        v-else-if="wizard.step.value === WizardStep.AnalysisError"
        key="analysis-error"
        v-bind="transition"
      >
        <ErrorState
          variant="analysis"
          :error-message="wizard.error.value ?? undefined"
          @retry="handleSubmitAndAnalyze"
          @go-back="handleStartOver"
        />
      </Motion>

      <!-- Empty Result -->
      <Motion
        v-else-if="wizard.step.value === WizardStep.EmptyResult"
        key="empty"
        v-bind="transition"
      >
        <EmptyState
          @new-match="handleStartOver"
          @go-home="handleStartOver"
        />
      </Motion>
    </AnimatePresence>
  </StepLayout>
</template>

<style scoped>
.step-content {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
  width: 100%;
}

.step-footer-row {
  display: flex;
  gap: 0.75rem;
  width: 100%;
}

.step-footer-col {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  width: 100%;
}
</style>
