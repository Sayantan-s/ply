<template>
  <main
    class="overflow-hidden flex items-center h-screen bg-white not-prose w-full items-center justify-center z-15 relative border-2 min-h-[200px] border-border bg-[linear-gradient(to_right,#8080804D_1px,transparent_1px),linear-gradient(to_bottom,#80808090_1px,transparent_1px)] shadow-shadow [background-size:30px_30px] bg-secondary-background"
  >
    <div class="w-full flex flex-col">
      <slot />
    </div>
  </main>
</template>

<script setup lang="ts">
import useMutation from "~/composables/hooks/useMutation";

interface IJDInputForm {
  jd: string;
  file: File | null;
}

interface IJDMatchStatusResponse {
  fileId: string;
}

defineOptions({ name: "ContextProvider" });

const [jdMatch, { loading }] = useMutation<IJDMatchStatusResponse>("/api/v1/jdmatch", "POST");
const form = useState<IJDInputForm>("jdInputForm", () => ({
  jd: "",
  file: null,
}));

const fileId = useState<string | null>("fileId", () => null);
const status = useState<JDMATCH_STATUS>("status", () => JDMATCH_STATUS.IDLE);
const jdMatchInfo = useState<JDMatchInfoResponse>("jdMatchInfo", () => ({}) as JDMatchInfoResponse);
</script>
