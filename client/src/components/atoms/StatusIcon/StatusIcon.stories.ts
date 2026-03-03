import type { Meta, StoryObj } from "@storybook/vue3-vite";
import StatusIcon from "./StatusIcon.vue";

const meta = {
  title: "Atoms/StatusIcon",
  component: StatusIcon,
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["error", "warning", "empty"],
    },
  },
} satisfies Meta<typeof StatusIcon>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Error: Story = {
  args: { variant: "error" },
};

export const Warning: Story = {
  args: { variant: "warning" },
};

export const Empty: Story = {
  args: { variant: "empty" },
};
