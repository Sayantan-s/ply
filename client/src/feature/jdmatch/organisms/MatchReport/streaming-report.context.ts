import type { ComputedRef, InjectionKey } from "vue";
import type { JdMatchStatus } from "../../types/api";

export type StreamingReportContext = {
  score: ComputedRef<number | null>;
  matchingSkills: ComputedRef<readonly string[] | null>;
  missingSkills: ComputedRef<readonly string[] | null>;
  streamedExplanation: ComputedRef<string>;
  isExplanationStreaming: ComputedRef<boolean>;
  currentStatus: ComputedRef<JdMatchStatus | null>;
  isLoading: ComputedRef<boolean>;
  isComplete: ComputedRef<boolean>;
};

export const STREAMING_REPORT_CONTEXT_KEY: InjectionKey<StreamingReportContext> =
  Symbol("streaming-report");
