import type { Meta, StoryObj } from "@storybook/vue3-vite";
import Alert from "./Alert.vue";

const meta = {
  title: "Atoms/Alert",
  component: Alert,
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["error", "warning", "info", "success"],
    },
  },
} satisfies Meta<typeof Alert>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Error: Story = {
  args: { variant: "error", message: "something went wrong with the operation." },
};

export const Warning: Story = {
  args: { variant: "warning", message: "this action may take longer than expected." },
};

export const Info: Story = {
  args: { variant: "info", message: "your inputs have been saved automatically." },
};

export const Success: Story = {
  args: { variant: "success", message: "analysis completed successfully." },
};
