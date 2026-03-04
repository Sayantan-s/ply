import type { Meta, StoryObj } from "@storybook/vue3-vite";
import CloudServicePicker from "./CloudServicePicker.vue";

const meta = {
  title: "JdMatch/Molecules/CloudServicePicker",
  component: CloudServicePicker,
  tags: ["autodocs"],
} satisfies Meta<typeof CloudServicePicker>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
