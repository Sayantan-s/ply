import type { Meta, StoryObj } from "@storybook/vue3-vite";
import Chip from "./Chip.vue";
import { HardDrive, Cloud } from "lucide-vue-next";
import { markRaw } from "vue";

const meta = {
  title: "Atoms/Chip",
  component: Chip,
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["active", "default"],
    },
  },
} satisfies Meta<typeof Chip>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Active: Story = {
  args: { variant: "active", label: "Active Chip", icon: markRaw(HardDrive) },
};

export const Default: Story = {
  args: { variant: "default", label: "Default Chip", icon: markRaw(Cloud) },
};
