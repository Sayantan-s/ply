import type { Meta, StoryObj } from "@storybook/vue3-vite";
import FinalReview from "./FinalReview.vue";

const meta = {
  title: "JdMatch/Organisms/FinalReview",
  component: FinalReview,
  tags: ["autodocs"],
  decorators: [
    () => ({
      template: '<div style="width: 440px;"><story /></div>',
    }),
  ],
} satisfies Meta<typeof FinalReview>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    fileName: "john_doe_resume_2024.pdf",
    fileSize: "245 KB",
    jdPreview: "Senior Frontend Engineer — Acme Corp",
  },
};
