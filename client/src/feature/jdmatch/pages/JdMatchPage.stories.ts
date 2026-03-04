import type { Meta, StoryObj } from "@storybook/vue3-vite";
import JdMatchPage from "./JdMatchPage.vue";

const meta = {
  title: "JdMatch/Pages/JdMatchPage",
  component: JdMatchPage,
  tags: ["autodocs"],
  parameters: {
    layout: "fullscreen",
  },
} satisfies Meta<typeof JdMatchPage>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {};
