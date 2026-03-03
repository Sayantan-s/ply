<script setup lang="ts">
import { ResultRatingCardLoading } from "#components";

interface IProps {
  data: JDMatchInfoResponse;
  loading: boolean;
}

const { data } = defineProps<IProps>();
</script>

<template>
  <div class="p-10 bg-amber-100">
    <ResultRatingCardLoading v-if="loading" />
    <ResultRatingCard
      v-if="!loading && data.score"
      :resume-name="data.file_name"
      :score="data.score"
    />
    <div class="mt-4">
      <ResultHeading text="Job Description" class="flex justify-end" />
      <textarea
        :value="data.jd"
        rows="10"
        class="w-full border-2 border-black p-4 resize-none outline-black bg-white"
        disabled
        readonly
      />
    </div>
    <div class="space-y-6">
      <div class="mt-4">
        <ResultHeading text="Matching Skills" />
        <ResultSkillCardLoading v-if="loading" :skills="12" />
        <ResultSkillCard v-if="!loading && data.matching_skills" :skills="data.matching_skills" />
      </div>
      <hr class="border-t-2 border-black" />
      <div>
        <ResultHeading text="Missing Skills" />
        <ResultSkillCardLoading v-if="loading" :skills="8" variant="secondary" />
        <ResultSkillCard v-if="!loading && data.missing_skills" :skills="data.missing_skills" />
      </div>
      <hr class="border-t-2 border-black" />

      <div>
        <ResultHeading text="Explanation" />
        <ResultExplanationLoading v-if="loading" />
        <ResultExplanation v-if="!loading && data.explanation" :value="data.explanation" />
      </div>
    </div>
  </div>
</template>
