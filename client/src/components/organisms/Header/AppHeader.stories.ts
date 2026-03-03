import type { Meta, StoryObj } from "@storybook/vue3-vite";
import AppHeader from "./AppHeader.vue";

const meta = {
  title: "Organisms/AppHeader",
  component: AppHeader,
  tags: ["autodocs"],
} satisfies Meta<typeof AppHeader>;

export default meta;
type Story = StoryObj<typeof meta>;

export const WithStep: Story = {
  args: { stepLabel: "01/03" },
};

export const NoStep: Story = {
  args: {},
};
