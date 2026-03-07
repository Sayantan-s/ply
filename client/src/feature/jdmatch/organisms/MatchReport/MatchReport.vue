<script setup lang="ts">
import { ref, markRaw } from "vue";
import { Motion } from "motion-v";
import { Download, Plus } from "lucide-vue-next";
import { ScoreRing, SkillItem, Modal, ModalHeader, ModalBody } from "@/components/molecules";
import { Button, ButtonIcon, ButtonContent, Text } from "@/components/atoms";
import type { MatchAnalysis } from "../../types/api";

defineProps<{
  analysis: MatchAnalysis;
}>();

defineEmits<{
  newMatch: [];
  download: [];
}>();

const DownloadIcon = markRaw(Download);
const PlusIcon = markRaw(Plus);

const summaryOpen = ref(false);

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
    <!-- Left Column: Score + Summary -->
    <div class="match-report__left">
      <div class="match-report__score">
        <ScoreRing :value="analysis.score" />
        <Text variant="label">match_score</Text>
      </div>
      <div class="match-report__summary">
        <Text variant="comment">// summary</Text>
        <p class="match-report__summary-text">
          {{ analysis.explanation }}
        </p>
        <button
          v-if="analysis.explanation.length > 0"
          class="match-report__read-more"
          @click="summaryOpen = true"
        >
          read_more
        </button>
      </div>
    </div>

    <!-- Right Column: Skills + Footer -->
    <div class="match-report__right">
      <div
        v-if="analysis.matchingSkills.length > 0"
        class="match-report__section"
      >
        <span class="match-report__section-title">matching_skills</span>
        <Motion
          as="div"
          initial="hidden"
          animate="visible"
          :variants="listVariants"
        >
          <Motion
            v-for="skill in analysis.matchingSkills"
            :key="skill"
            :variants="itemVariants"
          >
            <SkillItem variant="match" :skill="skill" />
          </Motion>
        </Motion>
      </div>

      <div
        v-if="analysis.missingSkills.length > 0"
        class="match-report__section"
      >
        <span class="match-report__section-title">missing_skills</span>
        <Motion
          as="div"
          initial="hidden"
          animate="visible"
          :variants="listVariants"
        >
          <Motion
            v-for="skill in analysis.missingSkills"
            :key="skill"
            :variants="itemVariants"
          >
            <SkillItem variant="missing" :skill="skill" />
          </Motion>
        </Motion>
      </div>

      <div class="match-report__divider" />
      <div class="match-report__footer">
        <Button variant="outline" fluid @click="$emit('download')">
          <ButtonIcon :icon="DownloadIcon" position="pre" :size="14" />
          <ButtonContent>Download Report</ButtonContent>
        </Button>
        <Button variant="primary" fluid @click="$emit('newMatch')">
          <ButtonIcon :icon="PlusIcon" position="pre" :size="14" />
          <ButtonContent>New Match</ButtonContent>
        </Button>
      </div>
    </div>

    <!-- Summary Modal -->
    <Modal v-model="summaryOpen" size="lg">
      <ModalHeader title="// summary" />
      <ModalBody>
        <p class="match-report__modal-text">{{ analysis.explanation }}</p>
      </ModalBody>
    </Modal>
  </div>
</template>

<style scoped>
.match-report {
  display: flex;
  gap: 2.5rem;
  width: 100%;
  max-width: 80rem;
}

.match-report__left {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
  flex: 0.5;
  flex-shrink: 0;
  background-color: var(--bg);
  padding: 1.25rem;
}

.match-report__right {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
  flex: 0.5;
  flex-shrink: 0;
  padding: 1.25rem;
}

.match-report__score {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem 0;
}

.match-report__summary {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background: var(--info-bg);
  border: 1px solid var(--info-border);
  padding: 1.25rem;
}

.match-report__summary-text {
  font-family: var(--font);
  font-size: 0.6875rem;
  font-weight: 400;
  line-height: 1.6;
  color: #444455;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 4;
  overflow: hidden;
}

.match-report__read-more {
  background: none;
  border: none;
  padding: 0;
  font-family: var(--font);
  font-size: 0.625rem;
  font-weight: 600;
  color: var(--accent);
  cursor: pointer;
}

.match-report__modal-text {
  font-family: var(--font);
  font-size: 0.8125rem;
  font-weight: 400;
  line-height: 1.7;
  color: var(--fg);
  white-space: pre-wrap;
  margin: 0;
}

.match-report__section {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.match-report__section-title {
  font-family: var(--font);
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--fg);
}

.match-report__divider {
  height: 1px;
  background: #e2e2e2;
  width: 100%;
}

.match-report__footer {
  display: flex;
  gap: 0.625rem;
  width: 100%;
}

@media (max-width: 768px) {
  .match-report {
    flex-direction: column;
    max-width: 100%;
  }

  .match-report__left,
  .match-report__right {
    width: 100%;
  }
}
</style>
