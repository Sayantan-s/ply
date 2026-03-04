<script setup lang="ts">
import { Motion } from "motion-v";
import { ScoreRing, SkillItem } from "@/components/molecules";
import { Alert, Heading, Text } from "@/components/atoms";
import type { MatchAnalysis } from "../../types/api";

defineProps<{
  analysis: MatchAnalysis;
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
  <div class="match-report">
    <div class="match-report__score">
      <ScoreRing :value="analysis.score" />
      <Text variant="label">Match Score</Text>
    </div>

    <div class="match-report__summary">
      <Text variant="comment">// summary</Text>
      <Alert variant="info" :message="analysis.explanation" />
    </div>

    <div v-if="analysis.matchingSkills.length > 0" class="match-report__section">
      <Heading :level="4">Matching Skills</Heading>
      <Motion as="div" initial="hidden" animate="visible" :variants="listVariants">
        <Motion
          v-for="skill in analysis.matchingSkills"
          :key="skill"
          :variants="itemVariants"
        >
          <SkillItem variant="match" :skill="skill" />
        </Motion>
      </Motion>
    </div>

    <div v-if="analysis.missingSkills.length > 0" class="match-report__section">
      <Heading :level="4">Missing Skills</Heading>
      <Motion as="div" initial="hidden" animate="visible" :variants="listVariants">
        <Motion
          v-for="skill in analysis.missingSkills"
          :key="skill"
          :variants="itemVariants"
        >
          <SkillItem variant="missing" :skill="skill" />
        </Motion>
      </Motion>
    </div>
  </div>
</template>

<style scoped>
.match-report {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  width: 100%;
}

.match-report__score {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1.5rem 0;
}

.match-report__summary {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.match-report__section {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
</style>
