import type { Meta, StoryObj } from "@storybook/vue3-vite";
import Dropzone from "./Dropzone.vue";

const meta = {
  title: "Molecules/Dropzone",
  component: Dropzone,
  tags: ["autodocs"],
} satisfies Meta<typeof Dropzone>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
};

export const CustomText: Story = {
  args: {
    primaryText: "upload your resume",
    secondaryText: ".pdf only — max 5mb",
  },
};
