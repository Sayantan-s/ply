<script setup lang="ts">
import { Motion } from "motion-v";
import { ScoreRing, SkillItem } from "@/components/molecules";
import { MatrixLoader, Text } from "@/components/atoms";
import type { JdMatchStatus } from "../../types/api";
import StreamingText from "../../molecules/StreamingText/StreamingText.vue";
import StatusMessage from "../../molecules/StatusMessage/StatusMessage.vue";

defineProps<{
  score: number | null;
  matchingSkills: readonly string[] | null;
  missingSkills: readonly string[] | null;
  streamedExplanation: string;
  isExplanationStreaming: boolean;
  currentStatus: JdMatchStatus | null;
}>();

const pulseTransition = {
  duration: 1.2,
  repeat: Infinity,
  repeatType: "reverse" as const,
};

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
    <!-- Status indicator (top) -->
    <div v-if="currentStatus" class="streaming-report__status">
      <MatrixLoader variant="text" size="md" tone="accent" />
      <StatusMessage :status="currentStatus" :is-active="true" />
    </div>

    <!-- Two-column layout -->
    <div class="streaming-report__columns">
    <!-- Left Column: Score + Summary -->
    <div class="streaming-report__left">
      <!-- Score: real or skeleton -->
      <div class="streaming-report__score">
        <template v-if="score !== null">
          <ScoreRing :value="score" />
          <Text variant="label">match_score</Text>
        </template>
        <template v-else>
          <Motion
            as="div"
            class="streaming-report__score-skeleton"
            :animate="{ opacity: [0.15, 0.35] }"
            :transition="pulseTransition"
          />
          <Motion
            as="div"
            class="streaming-report__bar--sm"
            :animate="{ opacity: [0.15, 0.35] }"
            :transition="pulseTransition"
          />
        </template>
      </div>

      <!-- Summary: streaming text or skeleton -->
      <div class="streaming-report__summary">
        <Text variant="comment">// summary</Text>
        <template v-if="streamedExplanation || isExplanationStreaming">
          <StreamingText
            :text="streamedExplanation"
            :is-streaming="isExplanationStreaming"
          />
        </template>
        <template v-else>
          <Motion
            v-for="i in 4"
            :key="`sum-${i}`"
            as="div"
            class="streaming-report__bar"
            :style="{ width: i === 4 ? '60%' : '100%' }"
            :animate="{ opacity: [0.15, 0.35] }"
            :transition="{ ...pulseTransition, delay: i * 0.1 }"
          />
        </template>
      </div>

    </div>

    <!-- Right Column: Skills -->
    <div class="streaming-report__right">
      <!-- Matching Skills: real or skeleton -->
      <template v-if="matchingSkills !== null">
        <div
          v-if="matchingSkills.length > 0"
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
              v-for="skill in matchingSkills"
              :key="skill"
              :variants="itemVariants"
            >
              <SkillItem variant="match" :skill="skill" />
            </Motion>
          </Motion>
        </div>
      </template>
      <div v-else class="streaming-report__section">
        <Motion
          as="div"
          class="streaming-report__bar--title"
          :animate="{ opacity: [0.15, 0.35] }"
          :transition="pulseTransition"
        />
        <Motion
          v-for="i in 3"
          :key="`ms-${i}`"
          as="div"
          class="streaming-report__chip"
          :animate="{ opacity: [0.15, 0.35] }"
          :transition="{ ...pulseTransition, delay: i * 0.1 }"
        />
      </div>

      <!-- Missing Skills: real or skeleton -->
      <template v-if="missingSkills !== null">
        <div
          v-if="missingSkills.length > 0"
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
              v-for="skill in missingSkills"
              :key="skill"
              :variants="itemVariants"
            >
              <SkillItem variant="missing" :skill="skill" />
            </Motion>
          </Motion>
        </div>
      </template>
      <div v-else class="streaming-report__section">
        <Motion
          as="div"
          class="streaming-report__bar--title"
          :animate="{ opacity: [0.15, 0.35] }"
          :transition="pulseTransition"
        />
        <Motion
          v-for="i in 2"
          :key="`mss-${i}`"
          as="div"
          class="streaming-report__chip"
          :animate="{ opacity: [0.15, 0.35] }"
          :transition="{ ...pulseTransition, delay: i * 0.1 }"
        />
      </div>
    </div>
    </div>
  </div>
</template>

<style scoped>
.streaming-report {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  width: 100%;
  max-width: 80rem;
}

.streaming-report__columns {
  display: flex;
  gap: 2.5rem;
  width: 100%;
}

.streaming-report__left {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
  flex: 0.5;
  flex-shrink: 0;
  background-color: var(--bg);
  padding: 1.25rem;
  height: max-content;
}

.streaming-report__right {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
  flex: 0.5;
  overflow: auto;
  flex-shrink: 0;
  padding: 1.25rem;
}

.streaming-report__score {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem 0;
}

.streaming-report__score-skeleton {
  width: 7.5rem;
  height: 7.5rem;
  border-radius: 50%;
  background: #e2e2e2;
}

.streaming-report__bar--sm {
  width: 4rem;
  height: 0.5rem;
  background: #e2e2e2;
  border-radius: 0.1875rem;
}

.streaming-report__summary {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background: var(--info-bg);
  border: 1px solid var(--info-border);
  padding: 1.25rem;
}

.streaming-report__bar {
  height: 0.625rem;
  background: #e2e2e2;
  border-radius: 0.1875rem;
  width: 100%;
}

.streaming-report__status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
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

.streaming-report__bar--title {
  width: 6rem;
  height: 0.75rem;
  background: #e2e2e2;
  border-radius: 0.1875rem;
}

.streaming-report__chip {
  height: 1.75rem;
  background: #e2e2e2;
  border-radius: 0.25rem;
  width: 80%;
}

@media (max-width: 768px) {
  .streaming-report__columns {
    flex-direction: column;
  }

  .streaming-report__left,
  .streaming-report__right {
    width: 100%;
  }
}
</style>
