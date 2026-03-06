export interface ResponseEnvelope<T> {
  success: boolean;
  data: T | null;
  error: string[] | null;
  requestId: string;
}

export interface ResumeUploadData {
  fileId: string;
  jdMatchId: string;
}

export interface JdMatchStatusData {
  status: JdMatchStatus;
}

export type JdMatchStatus =
  | "warming_up"
  | "lining_up"
  | "churning"
  | "combing"
  | "pondering"
  | "cooking"
  | "locked_in"
  | "fumbled";

export interface StatusStreamPayload {
  type: "status";
  status: JdMatchStatus;
}

export interface AnalysisStreamPayload {
  type: "analysis";
  chunk: string;
}

export interface ResultStreamPayload {
  type: "result";
  score: number;
  matchingSkills: string[];
  missingSkills: string[];
}

export interface ExplanationStreamPayload {
  type: "explanation";
  chunk: string;
}

export type StreamPayload =
  | StatusStreamPayload
  | AnalysisStreamPayload
  | ResultStreamPayload
  | ExplanationStreamPayload;

export interface JdMatchStreamLine {
  payload: StreamPayload;
}

export interface MatchAnalysis {
  score: number;
  matchingSkills: string[];
  missingSkills: string[];
  explanation: string;
}

export interface RawMatchAnalysis {
  score: number;
  matching_skills: string[];
  missing_skills: string[];
  explanation: string;
}

export interface JdMatchAnalysisData {
  jdMatchId: string;
  status: string;
  score: number | null;
  matchingSkills: string[] | null;
  missingSkills: string[] | null;
  explanation: string | null;
}

export interface CreateJdMatchPayload {
  resumeFile?: File;
  resumeUrl?: string;
  jdInfo?: string;
}
