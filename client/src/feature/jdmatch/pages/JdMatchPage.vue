<script setup lang="ts">
import { computed, markRaw } from "vue";
import { AnimatePresence, Motion } from "motion-v";
import { ArrowRight, ArrowLeft, Sparkles, Download, Plus, Share2 } from "lucide-vue-next";
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
const DownloadIcon = markRaw(Download);
const PlusIcon = markRaw(Plus);

const isSubmitting = computed(
  () => createMutation.isLoading.value || analyzeMutation.isStreaming.value,
);

const jdValidationError = computed(() => {
  if (jobDescription.jdText.value.length > 0 && jobDescription.jdText.value.trim().length < 50) {
    return "Job description must be at least 50 characters";
  }
  return undefined;
});

const transition = { initial: { opacity: 0, y: 16 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0, y: -16 }, transition: { duration: 0.25 } };
</script>

<template>
  <StepLayout :step-label="wizard.stepLabel.value">
    <template v-if="wizard.step.value === WizardStep.Report" #header-right>
      <button class="share-btn" aria-label="Share">
        <Share2 :size="16" />
      </button>
    </template>

    <AnimatePresence mode="wait">
      <!-- Step 1: Resume Upload -->
      <Motion
        v-if="wizard.step.value === WizardStep.ResumeUpload"
        key="step-1"
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
          @file-drop="resumeUpload.onFileDrop"
        />
      </Motion>

      <!-- Step 2: Job Description -->
      <Motion
        v-else-if="wizard.step.value === WizardStep.JobDescription"
        key="step-2"
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
          :jd-text-error="jdValidationError"
        />
      </Motion>

      <!-- Step 3: Final Review -->
      <Motion
        v-else-if="wizard.step.value === WizardStep.FinalReview"
        key="step-3"
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
      </Motion>

      <!-- Analyzing -->
      <Motion
        v-else-if="wizard.step.value === WizardStep.Analyzing"
        key="analyzing"
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
        <MatchReport :analysis="wizard.analysis.value" />
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
          @download="() => {}"
        />
      </Motion>
    </AnimatePresence>

    <template #footer>
      <!-- Step 1 Footer -->
      <Button
        v-if="wizard.step.value === WizardStep.ResumeUpload"
        variant="primary"
        fluid
        :disabled="!resumeUpload.isValid.value"
        @click="wizard.nextFromResume()"
      >
        Next: Job Description
        <component :is="ArrowRightIcon" :size="16" />
      </Button>

      <!-- Step 2 Footer -->
      <template v-if="wizard.step.value === WizardStep.JobDescription">
        <div class="footer-row">
          <Button variant="outline" @click="wizard.backToResume()">
            <component :is="ArrowLeftIcon" :size="14" />
            Back
          </Button>
          <Button
            variant="primary"
            :disabled="!jobDescription.isValid.value"
            @click="wizard.nextFromJd()"
          >
            Next: Preview
            <component :is="ArrowRightIcon" :size="16" />
          </Button>
        </div>
      </template>

      <!-- Step 3 Footer -->
      <template v-if="wizard.step.value === WizardStep.FinalReview">
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
          Go Back
        </Button>
      </template>

      <!-- Report Footer -->
      <template v-if="wizard.step.value === WizardStep.Report">
        <div class="footer-row">
          <Button variant="outline">
            <component :is="DownloadIcon" :size="14" />
            Download
          </Button>
          <Button variant="primary" @click="handleStartOver">
            <component :is="PlusIcon" :size="14" />
            New Match
          </Button>
        </div>
      </template>
    </template>
  </StepLayout>
</template>

<style scoped>
.footer-row {
  display: flex;
  gap: 0.75rem;
  width: 100%;
}

.footer-row > * {
  flex: 1;
}

.share-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--muted);
  padding: 0.25rem;
}

.share-btn:hover {
  color: var(--fg);
}
</style>
