import { computed } from "vue";
import { useQuery } from "@pinia/colada";
import type { MatchAnalysis } from "../types/api";
import { getJdMatchAnalysis } from "../api/jdmatch";

export function useJdMatchReport(jdMatchId: string) {
  const { data, status, error } = useQuery({
    key: () => ["jdmatch-analysis", jdMatchId],
    query: async () => {
      const response = await getJdMatchAnalysis(jdMatchId);
      if (!response.success || !response.data) {
        throw new Error(response.error?.[0] ?? "Failed to load report");
      }
      return response.data;
    },
  });

  const analysis = computed<MatchAnalysis | null>(() => {
    if (!data.value) return null;
    return {
      score: data.value.score ?? 0,
      matchingSkills: data.value.matchingSkills ?? [],
      missingSkills: data.value.missingSkills ?? [],
      explanation: data.value.explanation ?? "",
    };
  });

  const isLoading = computed(() => status.value === "pending");
  const isError = computed(() => status.value === "error");

  return {
    analysis,
    isLoading,
    isError,
    error,
  };
}
