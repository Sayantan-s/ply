<script lang="ts" setup>
import { LinkInput } from "#components";
import { useDataHandler, useDataSource } from "../context/DataProvider/hook";
import { ETAB } from "../context/DataProvider/types";

const { handleChange, handleReset, handleSubmit, handleChangeTabs } = useDataHandler();

const { tab, loading, jdMatchInfo, status, fileId, form, resumeLink } = useDataSource();

const computedStatusValues = computed(() => ({
  [JDMATCH_STATUS.MATCHED]: "bg-green-600",
  [JDMATCH_STATUS.FAILED]: "bg-rose-600",
}));

const baseFileInputStyles = computed(() => [
  "bg-black w-max px-4 py-3 border-2 border-black flex-1 flex flex-col justify-center",
  loading.value || fileId.value ? "hidden" : "",
]);

const baseButtonStyles = computed(() => [
  "border-2 justify-center px-8 py-2 border-black aspect-video text-shadow-md gap-2 flex items-center h-20",
  loading.value || fileId.value ? "flex-1" : "",
  computedStatusValues.value[status.value as keyof typeof computedStatusValues.value] ??
    "bg-purple-600",
]);

const scoreTabStyles = computed(() => [
  "flex-1 flex items-center gap-2 justify-center py-4 bg-black border-b-2 border-black aria-selected:bg-amber-100 aria-selected:text-black disabled:text-white/40 text-white",
]);

const iconStyles = computed(() => ({
  [JDMATCH_STATUS.FAILED]: "uil:annoyed",
  [JDMATCH_STATUS.MATCHED]: "uil:check-circle",
}));

const icon = iconStyles.value[status.value as keyof typeof iconStyles.value];
</script>

<template>
  <TabsRoot
    :model-value="tab"
    class="max-w-[800px] max-h-[710px] overflow-y-scroll mx-auto w-full border-2 border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)]"
  >
    <TabsList class="flex">
      <TabsTrigger
        :value="ETAB.TAB_1"
        class="flex-1 flex items-center gap-2 justify-center py-4 bg-black text-white border-b-2 border-black aria-selected:bg-amber-100 aria-selected:text-black"
        @click="handleChangeTabs(ETAB.TAB_1)"
      >
        <Icon name="uil:process" class="size-6" />
        Process
      </TabsTrigger>
      <TabsTrigger
        :value="ETAB.TAB_2"
        :disabled="loading || !jdMatchInfo.score"
        :class="scoreTabStyles"
        @click="handleChangeTabs(ETAB.TAB_2)"
      >
        Score
        <Icon name="uil:chart-pie" class="size-6" />
      </TabsTrigger>
    </TabsList>
    <TabsContent :value="ETAB.TAB_1">
      <form class="p-10 bg-amber-100" @submit.prevent="handleSubmit">
        <textarea
          v-model.trim="form.jd"
          rows="18"
          placeholder="eg. Paste your JD link or Job Description here"
          class="w-full border-2 border-black p-4 mb-4 resize-none outline-black bg-white"
          :readonly="status !== JDMATCH_STATUS.IDLE || loading"
          tabindex="1"
        />
        <div class="flex justify-between">
          <div role="button" :class="baseFileInputStyles">
            <div class="flex items-end">
              <p v-show="form.file?.name" class="text-purple-400">
                {{ form.file?.name }}
              </p>
              <div v-show="!form.file?.name">
                <p class="text-white flex items-center">
                  <FileInput
                    accept="application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/msword"
                    @change="handleChange"
                  >
                    <template #default="{ trigger }">
                      <button class="text-purple-400" @click="trigger">Attatch Resume</button>
                    </template>
                  </FileInput>
                  &nbsp;
                  <span>or</span>
                  &nbsp;
                  <LinkInput v-model="resumeLink" />
                </p>
              </div>
            </div>
            <div class="mt-1">
              <p v-if="form.file" class="text-xs text-gray-100">
                <span class="text-gray-500">File size:</span>
                {{ (form.file.size / 1024 / 1024).toFixed(2) }} MB
              </p>
              <p v-else class="text-xs text-gray-100">
                <span class="text-gray-500">PDF, DOC, DOCX.</span>
                File size max 3mb
              </p>
            </div>
          </div>
          <button
            :class="baseButtonStyles"
            :disabled="
              loading ||
              (!!fileId && status !== JDMATCH_STATUS.MATCHED) ||
              (!!fileId && status !== JDMATCH_STATUS.FAILED)
            "
          >
            <Loading
              v-if="
                loading ||
                (!!fileId && status !== JDMATCH_STATUS.MATCHED && status !== JDMATCH_STATUS.FAILED)
              "
            />
            <Icon v-if="icon" :name="icon" class="size-7 text-black" />
            {{ loading ? "Processing" : fileId ? JDMATCH_STATUS_TEXT[status] : "Proceed" }}
          </button>
          <button
            v-if="status === JDMATCH_STATUS.FAILED || status === JDMATCH_STATUS.MATCHED"
            class="px-6 py-3 border-2 border-l-0 border-black min-w-xl bg-black text-white"
            @click="handleReset"
          >
            Reset
          </button>
        </div>
      </form>
    </TabsContent>
    <TabsContent :value="ETAB.TAB_2">
      <Result :data="jdMatchInfo" :loading="loading || status !== JDMATCH_STATUS.MATCHED" />
    </TabsContent>
  </TabsRoot>
</template>
