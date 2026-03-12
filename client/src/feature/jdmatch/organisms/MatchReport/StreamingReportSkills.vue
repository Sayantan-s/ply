<script setup lang="ts">
import { inject } from "vue";
import { Motion } from "motion-v";
import { SkillItem } from "@/components/molecules";
import { STREAMING_REPORT_CONTEXT_KEY } from "./streaming-report.context";

const ctx = inject(STREAMING_REPORT_CONTEXT_KEY)!;

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
  <div class="streaming-report-skills">
    <!-- Matching Skills -->
    <template v-if="ctx.matchingSkills.value !== null">
      <Motion
        v-if="ctx.matchingSkills.value.length > 0"
        as="div"
        class="streaming-report-skills__section"
        :initial="{ opacity: 0 }"
        :animate="{ opacity: 1 }"
        :transition="{ duration: 0.25 }"
      >
        <span class="streaming-report-skills__title">matching_skills</span>
        <Motion
          as="div"
          initial="hidden"
          animate="visible"
          :variants="listVariants"
        >
          <Motion
            v-for="skill in ctx.matchingSkills.value"
            :key="skill"
            :variants="itemVariants"
          >
            <SkillItem variant="match" :skill="skill" />
          </Motion>
        </Motion>
      </Motion>
    </template>

    <div v-else class="streaming-report-skills__section">
      <Motion
        as="div"
        class="streaming-report-skills__bar-title"
        :animate="{ opacity: [0.15, 0.35] }"
        :transition="pulseTransition"
      />
      <Motion
        v-for="i in 3"
        :key="`ms-${i}`"
        as="div"
        class="streaming-report-skills__chip"
        :animate="{ opacity: [0.15, 0.35] }"
        :transition="{ ...pulseTransition, delay: i * 0.1 }"
      />
    </div>

    <!-- Missing Skills -->
    <template v-if="ctx.missingSkills.value !== null">
      <Motion
        v-if="ctx.missingSkills.value.length > 0"
        as="div"
        class="streaming-report-skills__section"
        :initial="{ opacity: 0 }"
        :animate="{ opacity: 1 }"
        :transition="{ duration: 0.25 }"
      >
        <span class="streaming-report-skills__title">missing_skills</span>
        <Motion
          as="div"
          initial="hidden"
          animate="visible"
          :variants="listVariants"
        >
          <Motion
            v-for="skill in ctx.missingSkills.value"
            :key="skill"
            :variants="itemVariants"
          >
            <SkillItem variant="missing" :skill="skill" />
          </Motion>
        </Motion>
      </Motion>
    </template>

    <div v-else class="streaming-report-skills__section">
      <Motion
        as="div"
        class="streaming-report-skills__bar-title"
        :animate="{ opacity: [0.15, 0.35] }"
        :transition="pulseTransition"
      />
      <Motion
        v-for="i in 2"
        :key="`mss-${i}`"
        as="div"
        class="streaming-report-skills__chip"
        :animate="{ opacity: [0.15, 0.35] }"
        :transition="{ ...pulseTransition, delay: i * 0.1 }"
      />
    </div>
  </div>
</template>

<style scoped>
.streaming-report-skills {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.streaming-report-skills__section {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
}

.streaming-report-skills__title {
  font-family: var(--font);
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--fg);
}

.streaming-report-skills__bar-title {
  width: 6rem;
  height: 0.75rem;
  background: #e2e2e2;
  border-radius: 0.1875rem;
}

.streaming-report-skills__chip {
  height: 1.75rem;
  background: #e2e2e2;
  border-radius: 0.25rem;
  width: 80%;
}
</style>
