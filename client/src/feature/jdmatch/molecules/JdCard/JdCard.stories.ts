import type { Meta, StoryObj } from "@storybook/vue3-vite";
import JdCard from "./JdCard.vue";

const meta = {
  title: "JdMatch/Molecules/JdCard",
  component: JdCard,
  tags: ["autodocs"],
  decorators: [
    () => ({
      template: '<div style="width: 440px;"><story /></div>',
    }),
  ],
} satisfies Meta<typeof JdCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    jdPreview: "Senior Frontend Engineer — Acme Corp",
  },
};
