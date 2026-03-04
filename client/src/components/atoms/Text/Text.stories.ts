import type { Meta, StoryObj } from "@storybook/vue3-vite";
import Text from "./Text.vue";

const meta = {
  title: "Atoms/Text",
  component: Text,
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["body", "label", "comment", "caption", "muted"],
    },
    as: {
      control: "select",
      options: ["p", "span", "label", "div"],
    },
  },
} satisfies Meta<typeof Text>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Body: Story = {
  args: { variant: "body" },
  render: (args) => ({
    components: { Text },
    setup: () => ({ args }),
    template: '<Text v-bind="args">Body text for descriptions and content.</Text>',
  }),
};

export const Label: Story = {
  args: { variant: "label" },
  render: (args) => ({
    components: { Text },
    setup: () => ({ args }),
    template: '<Text v-bind="args">field_label</Text>',
  }),
};

export const Comment: Story = {
  args: { variant: "comment" },
  render: (args) => ({
    components: { Text },
    setup: () => ({ args }),
    template: '<Text v-bind="args">// step_01</Text>',
  }),
};

export const Caption: Story = {
  args: { variant: "caption" },
  render: (args) => ({
    components: { Text },
    setup: () => ({ args }),
    template: '<Text v-bind="args">.pdf .docx — max 10mb</Text>',
  }),
};

export const AsSpan: Story = {
  args: { variant: "body", as: "span" },
  render: (args) => ({
    components: { Text },
    setup: () => ({ args }),
    template: '<Text v-bind="args">Inline text as a span</Text>',
  }),
};
