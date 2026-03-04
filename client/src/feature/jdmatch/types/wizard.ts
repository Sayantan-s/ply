import type { JdMatchStatus, MatchAnalysis } from "./api";

export enum WizardStep {
  ResumeUpload = "resume-upload",
  JobDescription = "job-description",
  FinalReview = "final-review",
  Analyzing = "analyzing",
  Report = "report",
  UploadError = "upload-error",
  AnalysisError = "analysis-error",
  EmptyResult = "empty-result",
}

export type ResumeSource = { type: "file"; file: File } | { type: "url"; url: string };

export interface WizardState {
  step: WizardStep;
  resume: ResumeSource | null;
  jdText: string;
  jdUrl: string;
  jdMatchId: string | null;
  fileId: string | null;
  analysis: MatchAnalysis | null;
  error: string | null;
  currentStatus: JdMatchStatus | null;
}
