import { ref, computed, readonly } from "vue";
import { WizardStep, type ResumeSource } from "../types/wizard";
import type { MatchAnalysis, JdMatchStatus } from "../types/api";

export function useJdMatchWizard() {
  const step = ref<WizardStep>(WizardStep.ResumeUpload);
  const resume = ref<ResumeSource | null>(null);
  const jdMatchId = ref<string | null>(null);
  const fileId = ref<string | null>(null);
  const analysis = ref<MatchAnalysis | null>(null);
  const error = ref<string | null>(null);
  const currentStatus = ref<JdMatchStatus | null>(null);

  const stepNumber = computed(() => {
    const map: Partial<Record<WizardStep, number>> = {
      [WizardStep.ResumeUpload]: 1,
      [WizardStep.JobDescription]: 2,
      [WizardStep.FinalReview]: 3,
    };
    return map[step.value] ?? null;
  });

  const stepLabel = computed(() => (stepNumber.value ? `0${stepNumber.value}/03` : null));

  // Navigation
  function nextFromResume() {
    step.value = WizardStep.JobDescription;
  }
  function nextFromJd() {
    step.value = WizardStep.FinalReview;
  }
  function backToResume() {
    step.value = WizardStep.ResumeUpload;
  }
  function backToJd() {
    step.value = WizardStep.JobDescription;
  }
  function startAnalysis() {
    step.value = WizardStep.Analyzing;
  }
  function showReport() {
    step.value = WizardStep.Report;
  }

  function showUploadError(msg: string) {
    error.value = msg;
    step.value = WizardStep.UploadError;
  }

  function showAnalysisError(msg: string) {
    error.value = msg;
    step.value = WizardStep.AnalysisError;
  }

  function showEmptyResult() {
    step.value = WizardStep.EmptyResult;
  }

  function startOver() {
    step.value = WizardStep.ResumeUpload;
    resume.value = null;
    jdMatchId.value = null;
    fileId.value = null;
    analysis.value = null;
    error.value = null;
    currentStatus.value = null;
  }

  // Setters
  function setResume(source: ResumeSource) {
    resume.value = source;
  }
  function setJdMatchResult(id: string, fId: string) {
    jdMatchId.value = id;
    fileId.value = fId;
  }
  function setAnalysis(result: MatchAnalysis) {
    analysis.value = result;
  }
  function setStatus(s: JdMatchStatus) {
    currentStatus.value = s;
  }

  return {
    step: readonly(step),
    resume: readonly(resume),
    jdMatchId: readonly(jdMatchId),
    fileId: readonly(fileId),
    analysis: readonly(analysis),
    error: readonly(error),
    currentStatus: readonly(currentStatus),
    stepNumber,
    stepLabel,
    nextFromResume,
    nextFromJd,
    backToResume,
    backToJd,
    startAnalysis,
    showReport,
    showUploadError,
    showAnalysisError,
    showEmptyResult,
    startOver,
    setResume,
    setJdMatchResult,
    setAnalysis,
    setStatus,
  };
}
