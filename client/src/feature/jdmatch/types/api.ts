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

// --- SSE Event Types ---

export type SSEEventType =
  | "analysis_start"
  | "status_update"
  | "content_block_start"
  | "content_block_delta"
  | "content_block_stop"
  | "analysis_delta"
  | "analysis_stop"
  | "error";

export type ContentBlockType = "result" | "explanation";

export type StopReason = "complete" | "error";

// --- Delta Types ---

export interface ResultDelta {
  type: "result_delta";
  score: number;
  matchingSkills: string[];
  missingSkills: string[];
}

export interface TextDelta {
  type: "text_delta";
  text: string;
}

export type Delta = ResultDelta | TextDelta;

// --- Content Block Markers ---

export interface ResultContentBlock {
  type: "result";
}

export interface ExplanationContentBlock {
  type: "explanation";
}

export type ContentBlock = ResultContentBlock | ExplanationContentBlock;

// --- SSE Event Models ---

export interface AnalysisStartEvent {
  type: "analysis_start";
  analysisId: string;
}

export interface StatusUpdateEvent {
  type: "status_update";
  status: JdMatchStatus;
}

export interface ContentBlockStartEvent {
  type: "content_block_start";
  index: number;
  contentBlock: ContentBlock;
}

export interface ContentBlockDeltaEvent {
  type: "content_block_delta";
  index: number;
  delta: Delta;
}

export interface ContentBlockStopEvent {
  type: "content_block_stop";
  index: number;
}

export interface AnalysisDeltaEvent {
  type: "analysis_delta";
  stopReason: StopReason;
}

export interface AnalysisStopEvent {
  type: "analysis_stop";
}

export interface ErrorEvent {
  type: "error";
  message: string;
}

export type SSEEvent =
  | AnalysisStartEvent
  | StatusUpdateEvent
  | ContentBlockStartEvent
  | ContentBlockDeltaEvent
  | ContentBlockStopEvent
  | AnalysisDeltaEvent
  | AnalysisStopEvent
  | ErrorEvent;

export interface ParsedSSEEvent {
  event: SSEEventType;
  data: SSEEvent;
}

// --- Non-streaming Types (unchanged) ---

export interface MatchAnalysis {
  score: number;
  matchingSkills: readonly string[];
  missingSkills: readonly string[];
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
