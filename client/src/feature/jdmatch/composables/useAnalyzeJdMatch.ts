import { ref, readonly } from "vue";
import type {
  JdMatchStatus,
  MatchAnalysis,
  ContentBlockDeltaEvent,
  ContentBlockStartEvent,
} from "../types/api";
import { analyzeJdMatch } from "../api/jdmatch";

export interface PartialResult {
  score: number;
  matchingSkills: string[];
  missingSkills: string[];
}

export function useAnalyzeJdMatch() {
  const isStreaming = ref(false);
  const currentStatus = ref<JdMatchStatus | null>(null);
  const statusHistory = ref<JdMatchStatus[]>([]);
  const analysis = ref<MatchAnalysis | null>(null);
  const error = ref<string | null>(null);
  const analysisId = ref<string | null>(null);

  const partialResult = ref<PartialResult | null>(null);
  const streamedExplanation = ref("");
  const isExplanationStreaming = ref(false);

  async function execute(jdMatchId: string): Promise<MatchAnalysis | null> {
    isStreaming.value = true;
    error.value = null;
    statusHistory.value = [];
    analysis.value = null;
    currentStatus.value = null;
    analysisId.value = null;
    partialResult.value = null;
    streamedExplanation.value = "";
    isExplanationStreaming.value = false;

    try {
      for await (const { event, data } of analyzeJdMatch(jdMatchId)) {
        switch (event) {
          case "analysis_start":
            if (data.type === "analysis_start") {
              analysisId.value = data.analysisId;
            }
            break;

          case "status_update":
            if (data.type === "status_update") {
              currentStatus.value = data.status;
              statusHistory.value = [...statusHistory.value, data.status];
            }
            break;

          case "content_block_start": {
            const startData = data as ContentBlockStartEvent;
            if (startData.contentBlock.type === "explanation") {
              isExplanationStreaming.value = true;
            }
            break;
          }

          case "content_block_delta": {
            const deltaData = data as ContentBlockDeltaEvent;
            if (deltaData.delta.type === "result_delta") {
              partialResult.value = {
                score: deltaData.delta.score,
                matchingSkills: deltaData.delta.matchingSkills,
                missingSkills: deltaData.delta.missingSkills,
              };
            } else if (deltaData.delta.type === "text_delta") {
              streamedExplanation.value += deltaData.delta.text;
            }
            break;
          }

          case "content_block_stop": {
            const stopData = data as { type: "content_block_stop"; index: number };
            if (stopData.index === 1) {
              isExplanationStreaming.value = false;
            }
            break;
          }

          case "error":
            if (data.type === "error") {
              error.value = data.message;
              return null;
            }
            break;

          case "analysis_delta":
          case "analysis_stop":
            break;
        }
      }

      // Build final analysis
      if (partialResult.value) {
        analysis.value = {
          score: partialResult.value.score,
          matchingSkills: [...partialResult.value.matchingSkills],
          missingSkills: [...partialResult.value.missingSkills],
          explanation: streamedExplanation.value,
        };
      }

      return analysis.value;
    } catch (e) {
      error.value = e instanceof Error ? e.message : "Analysis failed";
      return null;
    } finally {
      isStreaming.value = false;
      isExplanationStreaming.value = false;
    }
  }

  return {
    execute,
    isStreaming: readonly(isStreaming),
    currentStatus: readonly(currentStatus),
    statusHistory: readonly(statusHistory),
    analysis: readonly(analysis),
    error: readonly(error),
    analysisId: readonly(analysisId),
    partialResult: readonly(partialResult),
    streamedExplanation: readonly(streamedExplanation),
    isExplanationStreaming: readonly(isExplanationStreaming),
  };
}
