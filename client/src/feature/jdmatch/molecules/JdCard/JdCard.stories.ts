import type { Meta, StoryObj } from "@storybook/vue3-vite";
import JdCard from "./JdCard.vue";

const meta = {
  title: "JdMatch/Molecules/JdCard",
  component: JdCard,
  tags: ["autodocs"],
} satisfies Meta<typeof JdCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    jdPreview:
      "We are looking for a Senior Frontend Engineer with 5+ years of experience in React or Vue. The ideal candidate will have strong TypeScript skills...",
  },
};
