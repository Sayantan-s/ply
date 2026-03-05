import type { Meta, StoryObj } from "@storybook/vue3-vite";
import EmptyState from "./EmptyState.vue";

const meta = {
  title: "JdMatch/Organisms/EmptyState",
  component: EmptyState,
  tags: ["autodocs"],
  decorators: [
    () => ({
      template: '<div style="width: 400px;"><story /></div>',
    }),
  ],
} satisfies Meta<typeof EmptyState>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
