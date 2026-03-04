import type { Meta, StoryObj } from "@storybook/vue3-vite";
import FinalReview from "./FinalReview.vue";

const meta = {
  title: "JdMatch/Organisms/FinalReview",
  component: FinalReview,
  tags: ["autodocs"],
} satisfies Meta<typeof FinalReview>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    fileName: "sarah_chen_resume.pdf",
    fileSize: "2.3 MB",
    jdPreview:
      "We are looking for a Senior Frontend Engineer with 5+ years of experience in React or Vue. The ideal candidate will have strong TypeScript skills...",
  },
};
