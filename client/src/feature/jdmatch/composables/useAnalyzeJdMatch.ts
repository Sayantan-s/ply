import { ref, readonly } from "vue";
import type { JdMatchStatus, MatchAnalysis, RawMatchAnalysis } from "../types/api";
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

  const partialResult = ref<PartialResult | null>(null);
  const streamedExplanation = ref("");
  const isExplanationStreaming = ref(false);

  async function execute(jdMatchId: string): Promise<MatchAnalysis | null> {
    isStreaming.value = true;
    error.value = null;
    statusHistory.value = [];
    analysis.value = null;
    currentStatus.value = null;
    partialResult.value = null;
    streamedExplanation.value = "";
    isExplanationStreaming.value = false;

    const chunks: string[] = [];

    try {
      for await (const line of analyzeJdMatch(jdMatchId)) {
        const { payload } = line;

        if (payload.type === "status") {
          currentStatus.value = payload.status;
          statusHistory.value = [...statusHistory.value, payload.status];

          if (payload.status === "fumbled") {
            error.value = "Analysis failed";
            return null;
          }
        } else if (payload.type === "result") {
          partialResult.value = {
            score: payload.score,
            matchingSkills: payload.matchingSkills,
            missingSkills: payload.missingSkills,
          };
          isExplanationStreaming.value = true;
        } else if (payload.type === "explanation") {
          streamedExplanation.value += payload.chunk;
        } else if (payload.type === "analysis") {
          // Backward compat: old-style JSON chunks
          chunks.push(payload.chunk);
        }
      }

      isExplanationStreaming.value = false;

      // Build final analysis from new split flow or legacy flow
      if (partialResult.value) {
        analysis.value = {
          score: partialResult.value.score,
          matchingSkills: [...partialResult.value.matchingSkills],
          missingSkills: [...partialResult.value.missingSkills],
          explanation: streamedExplanation.value,
        };
      } else {
        const rawJson = chunks.join("");
        if (rawJson) {
          const raw: RawMatchAnalysis = JSON.parse(rawJson);
          analysis.value = {
            score: raw.score,
            matchingSkills: raw.matching_skills,
            missingSkills: raw.missing_skills,
            explanation: raw.explanation,
          };
        }
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
    partialResult: readonly(partialResult),
    streamedExplanation: readonly(streamedExplanation),
    isExplanationStreaming: readonly(isExplanationStreaming),
  };
}
