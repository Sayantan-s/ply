import type { Meta, StoryObj } from "@storybook/vue3-vite";
import JobDescriptionForm from "./JobDescriptionForm.vue";

const meta = {
  title: "JdMatch/Organisms/JobDescriptionForm",
  component: JobDescriptionForm,
  tags: ["autodocs"],
} satisfies Meta<typeof JobDescriptionForm>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    jdText: "",
    jdUrl: "",
  },
};

export const WithContent: Story = {
  args: {
    jdText:
      "We are looking for a Senior Frontend Engineer with 5+ years of experience in React or Vue. The ideal candidate will have strong TypeScript skills and experience building design systems.",
    jdUrl: "",
  },
};

export const WithError: Story = {
  args: {
    jdText: "Too short",
    jdUrl: "",
    jdTextError: "Job description must be at least 50 characters",
  },
};
