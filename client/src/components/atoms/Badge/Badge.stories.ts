import type { Meta, StoryObj } from "@storybook/vue3-vite";
import Badge from "./Badge.vue";

const meta = {
  title: "Atoms/Badge",
  component: Badge,
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["success", "error", "neutral"],
    },
  },
} satisfies Meta<typeof Badge>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Success: Story = {
  args: { variant: "success", label: "5+ yrs" },
};

export const Error: Story = {
  args: { variant: "error", label: "missing" },
};

export const Neutral: Story = {
  args: { variant: "neutral", label: "01/03" },
};
