import type { Meta, StoryObj } from "@storybook/vue3-vite";
import Heading from "./Heading.vue";

const meta = {
  title: "Atoms/Heading",
  component: Heading,
  tags: ["autodocs"],
  argTypes: {
    level: {
      control: "select",
      options: [1, 2, 3, 4, 5, 6],
    },
  },
} satisfies Meta<typeof Heading>;

export default meta;
type Story = StoryObj<typeof meta>;

export const H1: Story = {
  args: { level: 1 },
  render: (args) => ({
    components: { Heading },
    setup: () => ({ args }),
    template: '<Heading v-bind="args">Page Heading</Heading>',
  }),
};

export const H2: Story = {
  args: { level: 2 },
  render: (args) => ({
    components: { Heading },
    setup: () => ({ args }),
    template: '<Heading v-bind="args">Section Title</Heading>',
  }),
};

export const H3: Story = {
  args: { level: 3 },
  render: (args) => ({
    components: { Heading },
    setup: () => ({ args }),
    template: '<Heading v-bind="args">matching_skills</Heading>',
  }),
};
