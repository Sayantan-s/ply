import type { Meta, StoryObj } from "@storybook/vue3-vite";
import ErrorState from "./ErrorState.vue";

const meta = {
  title: "JdMatch/Organisms/ErrorState",
  component: ErrorState,
  tags: ["autodocs"],
} satisfies Meta<typeof ErrorState>;

export default meta;
type Story = StoryObj<typeof meta>;

export const UploadFailed: Story = {
  args: {
    variant: "upload",
    errorMessage:
      "unsupported_format — only .pdf and .docx files are accepted. Received .png (2.3mb)",
  },
};

export const AnalysisFailed: Story = {
  args: {
    variant: "analysis",
    errorMessage:
      "timeout_exceeded — The analysis engine did not respond within 30s. Your inputs have been saved — you can retry without re-uploading.",
  },
};
