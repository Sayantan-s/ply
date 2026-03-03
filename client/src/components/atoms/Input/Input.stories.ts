import type { Meta, StoryObj } from "@storybook/vue3-vite";
import Input from "./Input.vue";
import { Type } from "lucide-vue-next";
import { markRaw } from "vue";

const meta = {
  title: "Atoms/Input",
  component: Input,
  tags: ["autodocs"],
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
