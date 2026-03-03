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
import { ZodError } from "zod";
import useMutation from "~/composables/hooks/useMutation";
import { useSonner } from "../Sonner/hook";
import {
  dataHandlerInjectionKey,
  dataSourceInjectionKey,
  ETAB,
  type IJDInputForm,
  type IJDMatchStatusResponse,
} from "./types";

const [jdMatch, { loading }] = useMutation<IJDMatchStatusResponse>("/api/v1/jdmatch", "POST");
const form = useState<IJDInputForm>("jdInputForm", () => ({
  jd: "",
  file: null,
  cvLink: "",
}));

const resumeLink = useState<string>("resumeLink", () => "");

const fileId = useState<string | null>("fileId", () => null);
const status = useState<JDMATCH_STATUS>("status", () => JDMATCH_STATUS.IDLE);
const jdMatchInfo = useState<JDMatchInfoResponse>("jdMatchInfo", () => ({}) as JDMatchInfoResponse);

const tab = useState("tab", () => ETAB.TAB_1);

const handleChange = async (file: File | null) => {
  try {
    await jdDocSchema.parseAsync(file);
    form.value.file = file;
  } catch (err) {
    if (err instanceof ZodError) {
      console.error("Validation error:", err.errors);
    } else {
      console.error("Unexpected error:", err);
    }
  }
};

const { dispatchToast } = useSonner();

const handleSubmit = async () => {
  try {
    await jdFormSchema.parseAsync(form.value);
    const formData = new FormData();
    formData.append("url", form.value.jd);
    formData.append("file", form.value.file as Blob);
    const data = await jdMatch(formData);
    if (!data) return;
    fileId.value = data.fileId;
    await checkJDMatchStatus();
    await getJDMatchData();
  } catch (err) {
    if (err instanceof ZodError) {
      dispatchToast({
        variant: "warning",
        title: "Incorrect Input",
        description: err.errors.map((e) => e.message).join(", "),
      });
    } else {
      if (err === "jd_match_status") {
        dispatchToast({
          variant: "error",
          title: "JD Match Error",
          description: "Failed to generate JD match",
        });
      } else {
        dispatchToast({
          variant: "error",
          title: "Unexpected Error",
          description: "An unexpected error occurred",
        });
      }
    }
  } finally {
    loading.value = false;
  }
};

const checkJDMatchStatus = () =>
  new Promise<void>((resolve, reject) => {
    const interval = setInterval(async () => {
      try {
        const res = await $fetch(`/api/v1/jdmatch/status/${fileId.value}`, {
          method: "GET",
        });

        if (res && typeof res === "object" && res !== null && "status" in res) {
          status.value = res.status;
          if (res?.data?.jd) {
            jdMatchInfo!.value!.jd = res.data.jd;
            tab.value = ETAB.TAB_2;
          }
          if (status.value === JDMATCH_STATUS.MATCHED) {
            clearInterval(interval);
            resolve();
            dispatchToast({
              variant: "success",
              title: "Hurry!",
              description: "JD Match is complete",
            });
          }
        }
      } catch (error) {
        console.error("Error checking status:", error);
        status.value = JDMATCH_STATUS.FAILED;
        clearInterval(interval);
        reject("jd_match_status");
      }
    }, 1500);
  });

const getJDMatchData = async () => {
  try {
    const res = await $fetch(`/api/v1/jdmatch/score/${fileId.value}`, {
      method: "GET",
    });

    if (res && typeof res === "object" && res !== null) jdMatchInfo.value = res;
  } catch (error) {
    console.error("Error fetching JD match data:", error);
  }
};

const handleReset = (eve: Event) => {
  eve.preventDefault();
  eve.stopPropagation();
  fileId.value = null;
  status.value = JDMATCH_STATUS.IDLE;
  form.value.jd = "";
  form.value.file = null;
  jdMatchInfo.value.file_id = "";
  jdMatchInfo.value.score = 0;
  jdMatchInfo.value.matching_skills = [];
  jdMatchInfo.value.missing_skills = [];
  jdMatchInfo.value.explanation = "";
};

const handleChangeTabs = (value: ETAB) => {
  tab.value = value;
};

const dataHandlers = {
  handleSubmit,
  handleReset,
  handleChange,
  handleChangeTabs,
};

const data = {
  loading,
  jdMatchInfo,
  form,
  fileId,
  tab,
  status,
  resumeLink,
};

provide(dataSourceInjectionKey, data);
provide(dataHandlerInjectionKey, dataHandlers);
</script>
