import type { Meta, StoryObj } from "@storybook/vue3-vite";
import Dropzone from "./Dropzone.vue";

const meta = {
  title: "Molecules/Dropzone",
  component: Dropzone,
  tags: ["autodocs"],
  argTypes: {
    multiple: { control: "boolean" },
    maxSize: { control: { type: "number", min: 1, max: 100 } },
  },
} satisfies Meta<typeof Dropzone>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
};

export const PdfOnly: Story = {
  args: {
    formats: [".pdf"],
    maxSize: 5,
  },
};

export const Multiple: Story = {
  args: {
    multiple: true,
    formats: [".pdf", ".docx", ".txt"],
    maxSize: 20,
  },
};
