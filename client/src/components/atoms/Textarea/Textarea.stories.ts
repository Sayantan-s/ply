import type { Meta, StoryObj } from "@storybook/vue3-vite";
import Textarea from "./Textarea.vue";

const meta = {
  title: "Atoms/Textarea",
  component: Textarea,
  tags: ["autodocs"],
} satisfies Meta<typeof Textarea>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    label: "textarea_label",
    placeholder: "Write something here...",
  },
};

export const WithContent: Story = {
  args: {
    label: "textarea_label",
    placeholder: "Write something here...",
    modelValue: "Some content has been entered into this textarea field.",
  },
};
