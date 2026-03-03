import type { Meta, StoryObj } from "@storybook/vue3-vite";
import Button from "./Button.vue";
import { ArrowRight, Sparkles, Download } from "lucide-vue-next";
import { markRaw } from "vue";

const meta = {
  title: "Atoms/Button",
  component: Button,
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["primary", "accent", "outline", "ghost"],
    },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: { variant: "primary", label: "primary_action", icon: markRaw(ArrowRight) },
};

export const Accent: Story = {
  args: { variant: "accent", label: "accent_action", icon: markRaw(Sparkles) },
};

export const Outline: Story = {
  args: { variant: "outline", label: "outline_action", icon: markRaw(Download) },
};

export const Ghost: Story = {
  args: { variant: "ghost", label: "ghost_action" },
};
