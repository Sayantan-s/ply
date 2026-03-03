import type { Meta, StoryObj } from "@storybook/vue3-vite";
import SkillItem from "./SkillItem.vue";

const meta = {
  title: "Molecules/SkillItem",
  component: SkillItem,
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["match", "missing"],
    },
  },
} satisfies Meta<typeof SkillItem>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Match: Story = {
  args: {
    variant: "match",
    skill: "Skill Name",
    badge: "5+ yrs",
  },
};

export const Missing: Story = {
  args: {
    variant: "missing",
    skill: "Skill Name",
    detail: "Additional detail about the gap",
  },
};
