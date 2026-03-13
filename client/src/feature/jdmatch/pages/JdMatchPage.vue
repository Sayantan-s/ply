<script setup lang="ts">
import { computed, ref, watch, markRaw } from "vue";
import { AnimatePresence, Motion } from "motion-v";
import { ArrowRight, ArrowLeft, Sparkles, Link } from "lucide-vue-next";
import {
  Button,
  ButtonIcon,
  ButtonContent,
  ButtonLoading,
  Input,
  Textarea,
  Alert,
} from "@/components/atoms";
import {
  Dropzone,
  DropzoneEmpty,
  DropzoneFileList,
} from "@/components/molecules";
import { WizardStep } from "../types/wizard";
import { useJdMatchPage } from "../composables/useJdMatchPage";
import StepLayout from "../templates/StepLayout.vue";
import StepHeadline from "../molecules/StepHeadline/StepHeadline.vue";
import {
  WizardNavBarWizard,
  WizardNavBarReport,
  WizardNavBarEmpty,
} from "../molecules/WizardNavBar";
import ResumeUploadForm from "../organisms/ResumeUploadForm/ResumeUploadForm.vue";
import JobDescriptionForm from "../organisms/JobDescriptionForm/JobDescriptionForm.vue";
import FinalReview from "../organisms/FinalReview/FinalReview.vue";
import StreamingMatchReport from "../organisms/MatchReport/StreamingMatchReport.vue";
import StreamingReportStatus from "../organisms/MatchReport/StreamingReportStatus.vue";
import StreamingReportScore from "../organisms/MatchReport/StreamingReportScore.vue";
import StreamingReportSummary from "../organisms/MatchReport/StreamingReportSummary.vue";
import StreamingReportSkills from "../organisms/MatchReport/StreamingReportSkills.vue";
import StreamingReportActions from "../organisms/MatchReport/StreamingReportActions.vue";
import ErrorState from "../organisms/ErrorState/ErrorState.vue";
import EmptyState from "../organisms/EmptyState/EmptyState.vue";
import CloudServicePicker from "../molecules/CloudServicePicker/CloudServicePicker.vue";

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
const LinkIcon = markRaw(Link);

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

const isWizardStep = computed(
  () =>
    ![WizardStep.Analyzing, WizardStep.Report, WizardStep.EmptyResult].includes(
      wizard.step.value,
    ),
);
const isReportStep = computed(() => wizard.step.value === WizardStep.Report);
const isAnalyzing = computed(() => wizard.step.value === WizardStep.Analyzing);
const isEmptyStep = computed(
  () => wizard.step.value === WizardStep.EmptyResult,
);

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
  [
    WizardStep.UploadError,
    WizardStep.AnalysisError,
    WizardStep.EmptyResult,
  ].includes(wizard.step.value),
);

const cardWidth = computed(() => (isErrorOrEmpty.value ? 480 : undefined));
const noCard = computed(
  () =>
    wizard.step.value === WizardStep.Report ||
    wizard.step.value === WizardStep.Analyzing,
);

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
  <StepLayout :card-width="cardWidth" :no-card="noCard" :page="noCard">
    <template #nav>
      <WizardNavBarWizard v-if="isWizardStep" :active-step="activeNavStep" />
      <WizardNavBarEmpty v-else-if="isAnalyzing" />
      <WizardNavBarReport v-else-if="isReportStep" @back="handleStartOver" />
      <WizardNavBarEmpty v-else-if="isEmptyStep" @back="handleStartOver" />
    </template>

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
          v-model="resumeUpload.activeTab.value"
          :file-tab-disabled="resumeUpload.isFileTabDisabled.value"
          :url-tab-disabled="resumeUpload.isUrlTabDisabled.value"
        >
          <template #file>
            <Dropzone
              :model-value="resumeUpload.files.value"
              @update:model-value="resumeUpload.onFilesUpdate"
            >
              <DropzoneFileList />
              <DropzoneEmpty />
            </Dropzone>
            <span v-if="resumeUpload.errors.value.file" class="field-error">
              {{ resumeUpload.errors.value.file }}
            </span>
          </template>
          <template #url>
            <Input
              v-model="resumeUpload.resumeUrl.value"
              label="Resume URL"
              :placeholder="resumeUpload.urlPlaceholder.value"
              :icon="LinkIcon"
              :error="
                resumeUpload.errors.value.resumeUrl ??
                resumeUpload.urlDomainError.value
              "
            />
            <CloudServicePicker
              :model-value="resumeUpload.selectedService.value"
              @update:model-value="resumeUpload.selectedService.value = $event"
            />
            <Alert
              variant="info"
              message="Make sure the file has public or link-shared access enabled."
            />
          </template>
        </ResumeUploadForm>
        <Button
          variant="primary"
          fluid
          :disabled="!resumeUpload.isValid.value"
          @click="handleNextFromResume()"
        >
          <ButtonContent>next: job_description</ButtonContent>
          <ButtonIcon :icon="ArrowRightIcon" position="post" :size="14" />
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
        <JobDescriptionForm>
          <template #text-field>
            <Textarea
              v-model="jobDescription.jdText.value"
              label="Paste Job Description"
              placeholder="Paste the full JD content here..."
              :rows="8"
              :error="jobDescription.errors.value.jdText"
              :disabled="jobDescription.isJdTextDisabled.value"
            />
          </template>
          <template #url-field>
            <Input
              v-model="jobDescription.jdUrl.value"
              label="Job Post URL (optional)"
              placeholder="https://example.com/jobs/..."
              :icon="LinkIcon"
              :error="jobDescription.errors.value.jdUrl"
              :disabled="jobDescription.isJdUrlDisabled.value"
            />
          </template>
        </JobDescriptionForm>
        <div class="step-footer-row">
          <Button variant="outline" fluid @click="wizard.backToResume()">
            <ButtonIcon :icon="ArrowLeftIcon" position="pre" :size="14" />
            <ButtonContent>back</ButtonContent>
          </Button>
          <Button
            variant="primary"
            fluid
            :disabled="!jobDescription.isValid.value"
            @click="handleNextFromJd()"
          >
            <ButtonContent>next: review</ButtonContent>
            <ButtonIcon :icon="ArrowRightIcon" position="post" :size="14" />
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
            <ButtonLoading variant="grid">analyzing...</ButtonLoading>
            <ButtonIcon :icon="SparklesIcon" position="pre" :size="14" />
            <ButtonContent>Run Match Report</ButtonContent>
          </Button>
          <Button variant="ghost" fluid @click="wizard.backToJd()">
            <ButtonContent>go_back</ButtonContent>
          </Button>
        </div>
      </Motion>

      <!-- Analyzing: unified progressive view -->
      <Motion
        v-else-if="
          wizard.step.value === WizardStep.Analyzing ||
          (wizard.step.value === WizardStep.Report && wizard.analysis.value)
        "
        key="analyzing"
        v-bind="transition"
      >
        <StreamingMatchReport
          :score="analyzeMutation.partialResult.value?.score ?? null"
          :matching-skills="
            analyzeMutation.partialResult.value?.matchingSkills ?? null
          "
          :missing-skills="
            analyzeMutation.partialResult.value?.missingSkills ?? null
          "
          :streamed-explanation="analyzeMutation.streamedExplanation.value"
          :is-explanation-streaming="
            analyzeMutation.isExplanationStreaming.value
          "
          :current-status="analyzeMutation.currentStatus.value"
        >
          <StreamingReportStatus />
          <div class="analysis-columns">
            <div class="analysis-columns__left">
              <StreamingReportScore />
              <StreamingReportSummary />
            </div>
            <div class="analysis-columns__right">
              <StreamingReportSkills />
              <StreamingReportActions
                @download="() => {}"
                @new-match="handleStartOver"
              />
            </div>
          </div>
        </StreamingMatchReport>
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
        <EmptyState @new-match="handleStartOver" @go-home="handleStartOver" />
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

.field-error {
  font-family: var(--font);
  font-size: 0.625rem;
  font-weight: 400;
  color: var(--error);
}

.analysis-columns {
  display: flex;
  gap: 1.5rem;
  width: 100%;
  position: relative;
}

.analysis-columns__left {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  flex: 0.5;
  flex-shrink: 0;
  height: max-content;
  position: relative;
}

.analysis-columns__right {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
  flex: 0.5;
  overflow: auto;
  flex-shrink: 0;
  padding: 1.25rem;
  background-color: var(--bg);
  height: max-content;
  position: sticky;
  top: 1.5rem;
}

@media (max-width: 768px) {
  .analysis-columns {
    flex-direction: column;
  }

  .analysis-columns__left,
  .analysis-columns__right {
    width: 100%;
  }
}
</style>
