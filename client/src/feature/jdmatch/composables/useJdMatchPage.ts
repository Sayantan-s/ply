import type { CreateJdMatchPayload } from "../types/api";
import { useJdMatchWizard } from "./useJdMatchWizard";
import { useResumeUpload } from "./useResumeUpload";
import { useJobDescription } from "./useJobDescription";
import { useCreateJdMatch } from "./useCreateJdMatch";
import { useAnalyzeJdMatch } from "./useAnalyzeJdMatch";

export function useJdMatchPage() {
  const wizard = useJdMatchWizard();
  const resumeUpload = useResumeUpload();
  const jobDescription = useJobDescription();
  const createMutation = useCreateJdMatch();
  const analyzeMutation = useAnalyzeJdMatch();

  async function handleSubmitAndAnalyze() {
    if (!resumeUpload.resumeSource.value) return;

    const source = resumeUpload.resumeSource.value;
    wizard.setResume(source);

    const payload: CreateJdMatchPayload = {
      resumeFile: source.type === "file" ? source.file : undefined,
      resumeUrl: source.type === "url" ? source.url : undefined,
      jdInfo: jobDescription.jdText.value || jobDescription.jdUrl.value || undefined,
    };

    const result = await createMutation.execute(payload);
    if (!result) {
      wizard.showUploadError(createMutation.error.value ?? "Upload failed");
      return;
    }

    wizard.setJdMatchResult(result.jdMatchId, result.fileId);
    wizard.startAnalysis();

    const analysis = await analyzeMutation.execute(result.jdMatchId);
    if (!analysis) {
      wizard.showAnalysisError(analyzeMutation.error.value ?? "Analysis failed");
      return;
    }

    if (analysis.score === 0 && analysis.matchingSkills.length === 0) {
      wizard.setAnalysis(analysis);
      wizard.showEmptyResult();
      return;
    }

    wizard.setAnalysis(analysis);
    wizard.showReport();
  }

  function handleStartOver() {
    wizard.startOver();
    resumeUpload.reset();
    jobDescription.reset();
  }

  return {
    wizard,
    resumeUpload,
    jobDescription,
    createMutation,
    analyzeMutation,
    handleSubmitAndAnalyze,
    handleStartOver,
  };
}
