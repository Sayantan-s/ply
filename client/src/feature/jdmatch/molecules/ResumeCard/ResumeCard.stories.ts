import type { Meta, StoryObj } from "@storybook/vue3-vite";
import ResumeCard from "./ResumeCard.vue";

const meta = {
  title: "JdMatch/Molecules/ResumeCard",
  component: ResumeCard,
  tags: ["autodocs"],
  decorators: [
    () => ({
      template: '<div style="width: 440px;"><story /></div>',
    }),
  ],
} satisfies Meta<typeof ResumeCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    fileName: "john_doe_resume_2024.pdf",
    fileSize: "245 KB",
  },
};
