import type { Meta, StoryObj } from "@storybook/vue3-vite";
import ScoreRing from "./ScoreRing.vue";

const meta = {
  title: "Molecules/ScoreRing",
  component: ScoreRing,
  tags: ["autodocs"],
  argTypes: {
    value: { control: { type: "range", min: 0, max: 100 } },
  },
} satisfies Meta<typeof ScoreRing>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: { value: 78 },
};

export const Low: Story = {
  args: { value: 25 },
};

export const Full: Story = {
  args: { value: 100 },
};
