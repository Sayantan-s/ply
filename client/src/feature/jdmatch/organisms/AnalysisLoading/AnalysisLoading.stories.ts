import type { Meta, StoryObj } from "@storybook/vue3-vite";
import AnalysisLoading from "./AnalysisLoading.vue";

const meta = {
  title: "JdMatch/Organisms/AnalysisLoading",
  component: AnalysisLoading,
  tags: ["autodocs"],
} satisfies Meta<typeof AnalysisLoading>;

export default meta;
type Story = StoryObj<typeof meta>;

export const InProgress: Story = {
  args: {
    statusHistory: ["warming_up", "lining_up", "pondering"],
    currentStatus: "pondering",
  },
};

export const Cooking: Story = {
  args: {
    statusHistory: ["warming_up", "lining_up", "pondering", "cooking"],
    currentStatus: "cooking",
  },
};

export const Done: Story = {
  args: {
    statusHistory: ["warming_up", "lining_up", "pondering", "cooking", "locked_in"],
    currentStatus: "locked_in",
  },
};
