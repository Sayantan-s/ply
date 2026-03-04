import type { Meta, StoryObj } from "@storybook/vue3-vite";
import Textarea from "./Textarea.vue";

const meta = {
  title: "Atoms/Textarea",
  component: Textarea,
  tags: ["autodocs"],
  argTypes: {
    disabled: { control: "boolean" },
    rows: { control: { type: "number", min: 2, max: 20 } },
  },
} satisfies Meta<typeof Textarea>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    label: "paste_job_description",
    placeholder: "Write something here...",
  },
};

export const Tall: Story = {
  args: {
    label: "paste_job_description",
    placeholder: "Paste the full job description...",
    rows: 10,
  },
};

export const WithContent: Story = {
  args: {
    label: "paste_job_description",
    placeholder: "Write something here...",
    modelValue:
      "We are looking for a Senior Frontend Engineer with 5+ years of experience in React or Vue...",
    rows: 8,
  },
};

export const WithError: Story = {
  args: {
    label: "paste_job_description",
    placeholder: "Write something here...",
    modelValue: "too short",
    error: "minimum 50 characters required",
  },
};

export const Disabled: Story = {
  args: {
    label: "paste_job_description",
    placeholder: "Write something here...",
    disabled: true,
  },
};
