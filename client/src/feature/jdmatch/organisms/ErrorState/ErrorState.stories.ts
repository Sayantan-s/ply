import type { Meta, StoryObj } from "@storybook/vue3-vite";
import ErrorState from "./ErrorState.vue";

const meta = {
  title: "JdMatch/Organisms/ErrorState",
  component: ErrorState,
  tags: ["autodocs"],
  decorators: [
    () => ({
      template: '<div style="width: 400px;"><story /></div>',
    }),
  ],
} satisfies Meta<typeof ErrorState>;

export default meta;
type Story = StoryObj<typeof meta>;

export const UploadFailed: Story = {
  args: {
    variant: "upload",
    errorMessage: "ERR_INVALID_FORMAT: .docx files are not supported",
  },
};

export const AnalysisFailed: Story = {
  args: {
    variant: "analysis",
    errorMessage: "TIMEOUT_EXCEEDED: engine did not respond in time",
    requestId: "req_7f3a9b2c",
  },
};
