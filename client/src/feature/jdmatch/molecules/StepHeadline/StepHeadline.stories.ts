import type { Meta, StoryObj } from "@storybook/vue3-vite";
import StepHeadline from "./StepHeadline.vue";

const meta = {
  title: "JdMatch/Molecules/StepHeadline",
  component: StepHeadline,
  tags: ["autodocs"],
} satisfies Meta<typeof StepHeadline>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Step1: Story = {
  args: {
    stepComment: "// step_01",
    title: "Upload Resume",
    subtitle: "We'll analyze it against your target job description.",
  },
};

export const Step2: Story = {
  args: {
    stepComment: "// step_02",
    title: "Job Details",
    subtitle: "Paste the job description or provide the job post URL.",
  },
};

export const Step3: Story = {
  args: {
    stepComment: "// step_03",
    title: "Final Review",
    subtitle: "Confirm your inputs before running the analysis.",
  },
};
