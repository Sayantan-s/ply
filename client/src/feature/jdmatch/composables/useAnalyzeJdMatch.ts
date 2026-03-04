import { ref, readonly } from "vue";
import type { JdMatchStatus, MatchAnalysis, RawMatchAnalysis } from "../types/api";
import { analyzeJdMatch } from "../api/jdmatch";

export function useAnalyzeJdMatch() {
  const isStreaming = ref(false);
  const currentStatus = ref<JdMatchStatus | null>(null);
  const statusHistory = ref<JdMatchStatus[]>([]);
  const analysis = ref<MatchAnalysis | null>(null);
  const error = ref<string | null>(null);

  async function execute(jdMatchId: string): Promise<MatchAnalysis | null> {
    isStreaming.value = true;
    error.value = null;
    statusHistory.value = [];
    analysis.value = null;
    currentStatus.value = null;

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
        } else if (payload.type === "analysis") {
          chunks.push(payload.chunk);
        }
      }

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

      return analysis.value;
    } catch (e) {
      error.value = e instanceof Error ? e.message : "Analysis failed";
      return null;
    } finally {
      isStreaming.value = false;
    }
  }

  return {
    execute,
    isStreaming: readonly(isStreaming),
    currentStatus: readonly(currentStatus),
    statusHistory: readonly(statusHistory),
    analysis: readonly(analysis),
    error: readonly(error),
  };
}
