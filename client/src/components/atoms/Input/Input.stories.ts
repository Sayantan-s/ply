import type { Meta, StoryObj } from "@storybook/vue3-vite";
import Input from "./Input.vue";
import { Type, Link } from "lucide-vue-next";
import { markRaw } from "vue";

const meta = {
  title: "Atoms/Input",
  component: Input,
  tags: ["autodocs"],
  argTypes: {
    disabled: { control: "boolean" },
  },
} satisfies Meta<typeof Input>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    label: "field_label",
    placeholder: "placeholder_text",
    icon: markRaw(Type),
  },
};

export const Filled: Story = {
  args: {
    label: "field_label",
    placeholder: "placeholder_text",
    icon: markRaw(Type),
    modelValue: "filled_value",
  },
};

export const WithError: Story = {
  args: {
    label: "job_post_url",
    placeholder: "https://...",
    icon: markRaw(Link),
    modelValue: "not-a-valid-url",
    error: "invalid URL format",
  },
};

export const Disabled: Story = {
  args: {
    label: "resume_url",
    placeholder: "https://...",
    icon: markRaw(Link),
    disabled: true,
  },
};
