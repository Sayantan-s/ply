import type { Meta, StoryObj } from "@storybook/vue3-vite";
import StatusMessage from "./StatusMessage.vue";

const meta = {
  title: "JdMatch/Molecules/StatusMessage",
  component: StatusMessage,
  tags: ["autodocs"],
  argTypes: {
    status: {
      control: "select",
      options: [
        "warming_up",
        "lining_up",
        "churning",
        "combing",
        "pondering",
        "cooking",
        "locked_in",
        "fumbled",
      ],
    },
    isActive: { control: "boolean" },
  },
} satisfies Meta<typeof StatusMessage>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Active: Story = {
  args: { status: "pondering", isActive: true },
};

export const Inactive: Story = {
  args: { status: "warming_up", isActive: false },
};

export const LockedIn: Story = {
  args: { status: "locked_in", isActive: false },
};

export const Fumbled: Story = {
  args: { status: "fumbled", isActive: false },
};
