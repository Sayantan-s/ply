import type { Meta, StoryObj } from "@storybook/vue3-vite";
import ResumeCard from "./ResumeCard.vue";

const meta = {
  title: "JdMatch/Molecules/ResumeCard",
  component: ResumeCard,
  tags: ["autodocs"],
} satisfies Meta<typeof ResumeCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    fileName: "sarah_chen_resume.pdf",
    fileSize: "2.3 MB",
  },
};
