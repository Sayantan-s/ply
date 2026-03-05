import type { Meta, StoryObj } from "@storybook/vue3-vite";
import ResumeUploadForm from "./ResumeUploadForm.vue";
import { ref } from "vue";

const meta = {
  title: "JdMatch/Organisms/ResumeUploadForm",
  component: ResumeUploadForm,
  tags: ["autodocs"],
} satisfies Meta<typeof ResumeUploadForm>;

export default meta;
type Story = StoryObj<typeof meta>;

export const FileTab: Story = {
  render: () => ({
    components: { ResumeUploadForm },
    setup() {
      const activeTab = ref<"file" | "url">("file");
      const resumeUrl = ref("");
      const files = ref<File[]>([]);
      const selectedService = ref("");
      return { activeTab, resumeUrl, files, selectedService };
    },
    template: `
      <ResumeUploadForm
        v-model:active-tab="activeTab"
        v-model:resume-url="resumeUrl"
        :files="files"
        :selected-service="selectedService"
        @update:files="files = $event"
        @update:selected-service="selectedService = $event"
      />
    `,
  }),
};

export const UrlTab: Story = {
  render: () => ({
    components: { ResumeUploadForm },
    setup() {
      const activeTab = ref<"file" | "url">("url");
      const resumeUrl = ref("");
      const selectedService = ref("");
      return { activeTab, resumeUrl, selectedService };
    },
    template: `
      <ResumeUploadForm
        v-model:active-tab="activeTab"
        v-model:resume-url="resumeUrl"
        :selected-service="selectedService"
        @update:selected-service="selectedService = $event"
      />
    `,
  }),
};

export const WithUrlError: Story = {
  render: () => ({
    components: { ResumeUploadForm },
    setup() {
      const activeTab = ref<"file" | "url">("url");
      const resumeUrl = ref("https://onedrive.live.com/doc");
      const selectedService = ref("google-drive");
      return { activeTab, resumeUrl, selectedService };
    },
    template: `
      <ResumeUploadForm
        v-model:active-tab="activeTab"
        v-model:resume-url="resumeUrl"
        :selected-service="selectedService"
        url-error="URL must be from drive.google.com"
        @update:selected-service="selectedService = $event"
      />
    `,
  }),
};
