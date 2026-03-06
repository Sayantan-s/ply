<script setup lang="ts">
import { Motion } from "motion-v";
import { ScoreRing, SkillItem } from "@/components/molecules";
import { Text } from "@/components/atoms";
import StreamingText from "../../molecules/StreamingText/StreamingText.vue";

interface StreamingPartialResult {
  score: number;
  matchingSkills: readonly string[];
  missingSkills: readonly string[];
}

defineProps<{
  partialResult: StreamingPartialResult;
  streamedExplanation: string;
  isExplanationStreaming: boolean;
}>();

const listVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.08 } },
};

const itemVariants = {
  hidden: { opacity: 0, y: 8 },
  visible: { opacity: 1, y: 0 },
};
</script>

<template>
  <div class="streaming-report">
    <!-- Left Column: Score + Streaming Summary -->
    <div class="streaming-report__left">
      <div class="streaming-report__score">
        <ScoreRing :value="partialResult.score" />
        <Text variant="label">match_score</Text>
      </div>
      <div class="streaming-report__summary">
        <Text variant="comment">// summary</Text>
        <StreamingText
          :text="streamedExplanation"
          :is-streaming="isExplanationStreaming"
        />
      </div>
    </div>

    <!-- Right Column: Skills -->
    <div class="streaming-report__right">
      <div
        v-if="partialResult.matchingSkills.length > 0"
        class="streaming-report__section"
      >
        <span class="streaming-report__section-title">matching_skills</span>
        <Motion
          as="div"
          initial="hidden"
          animate="visible"
          :variants="listVariants"
        >
          <Motion
            v-for="skill in partialResult.matchingSkills"
            :key="skill"
            :variants="itemVariants"
          >
            <SkillItem variant="match" :skill="skill" />
          </Motion>
        </Motion>
      </div>

      <div
        v-if="partialResult.missingSkills.length > 0"
        class="streaming-report__section"
      >
        <span class="streaming-report__section-title">missing_skills</span>
        <Motion
          as="div"
          initial="hidden"
          animate="visible"
          :variants="listVariants"
        >
          <Motion
            v-for="skill in partialResult.missingSkills"
            :key="skill"
            :variants="itemVariants"
          >
            <SkillItem variant="missing" :skill="skill" />
          </Motion>
        </Motion>
      </div>
    </div>
  </div>
</template>

<style scoped>
.streaming-report {
  display: flex;
  gap: 2.5rem;
  width: 100%;
  max-width: 50rem;
}

.streaming-report__left {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
  width: 25rem;
  flex-shrink: 0;
  background-color: var(--bg);
  padding: 1.25rem;
  height: max-content;
}

.streaming-report__right {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
  width: 25rem;
  max-height: 20rem;
  overflow: auto;
  flex-shrink: 0;
  padding: 1.25rem;
  border: 1px solid var(--info-border);
}

.streaming-report__score {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem 0;
}

.streaming-report__summary {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background: var(--info-bg);
  border: 1px solid var(--info-border);
  padding: 1.25rem;
}

.streaming-report__section {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.streaming-report__section-title {
  font-family: var(--font);
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--fg);
}

@media (max-width: 768px) {
  .streaming-report {
    flex-direction: column;
    max-width: 100%;
  }

  .streaming-report__left,
  .streaming-report__right {
    width: 100%;
  }
}
</style>
