import type { Meta, StoryObj } from "@storybook/vue3-vite";
import ResumeUploadForm from "./ResumeUploadForm.vue";

const meta = {
  title: "JdMatch/Organisms/ResumeUploadForm",
  component: ResumeUploadForm,
  tags: ["autodocs"],
} satisfies Meta<typeof ResumeUploadForm>;

export default meta;
type Story = StoryObj<typeof meta>;

export const FileTab: Story = {
  args: {
    activeTab: "file",
    resumeUrl: "",
  },
};

export const UrlTab: Story = {
  args: {
    activeTab: "url",
    resumeUrl: "",
  },
};
