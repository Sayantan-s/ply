import type { Meta, StoryObj } from "@storybook/vue3-vite";
import Button from "./Button.vue";
import { ArrowRight, Sparkles, Download, ArrowLeft } from "lucide-vue-next";
import { markRaw } from "vue";

const meta = {
  title: "Atoms/Button",
  component: Button,
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["primary", "accent", "outline", "ghost"],
    },
    disabled: { control: "boolean" },
    loading: { control: "boolean" },
    fluid: { control: "boolean" },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Primary: Story = {
  args: { variant: "primary" },
  render: (args) => ({
    components: { Button, ArrowRight: markRaw(ArrowRight) },
    setup: () => ({ args }),
    template: '<Button v-bind="args">next: job_description <ArrowRight :size="16" /></Button>',
  }),
};

export const Accent: Story = {
  args: { variant: "accent" },
  render: (args) => ({
    components: { Button, Sparkles: markRaw(Sparkles) },
    setup: () => ({ args }),
    template: '<Button v-bind="args"><Sparkles :size="18" /> run_match_report</Button>',
  }),
};

export const Outline: Story = {
  args: { variant: "outline" },
  render: (args) => ({
    components: { Button, Download: markRaw(Download) },
    setup: () => ({ args }),
    template: '<Button v-bind="args"><Download :size="14" /> download</Button>',
  }),
};

export const Ghost: Story = {
  args: { variant: "ghost" },
  render: (args) => ({
    components: { Button },
    setup: () => ({ args }),
    template: '<Button v-bind="args">go_back</Button>',
  }),
};

export const Fluid: Story = {
  args: { variant: "primary", fluid: true },
  render: (args) => ({
    components: { Button, ArrowRight: markRaw(ArrowRight) },
    setup: () => ({ args }),
    template: `
      <div style="width: 24rem">
        <Button v-bind="args">next: job_description <ArrowRight :size="16" /></Button>
      </div>
    `,
  }),
};

export const Loading: Story = {
  args: { variant: "accent", loading: true, fluid: true },
  render: (args) => ({
    components: { Button },
    setup: () => ({ args }),
    template: `
      <div style="width: 24rem">
        <Button v-bind="args">analyzing...</Button>
      </div>
    `,
  }),
};

export const Loading2: Story = {
  args: {
    variant: "primary",
    loading: true,
    fluid: true,
    loaderVariant: "grid",
  },
  render: (args) => ({
    components: { Button },
    setup: () => ({ args }),
    template: `
      <div style="width: 24rem">
        <Button v-bind="args">analyzing...</Button>
      </div>
    `,
  }),
};

export const Disabled: Story = {
  args: { variant: "primary", disabled: true, fluid: true },
  render: (args) => ({
    components: { Button, ArrowRight: markRaw(ArrowRight) },
    setup: () => ({ args }),
    template: `
      <div style="width: 24rem">
        <Button v-bind="args">next: job_description <ArrowRight :size="16" /></Button>
      </div>
    `,
  }),
};

export const BackOutline: Story = {
  args: { variant: "outline", fluid: true },
  render: (args) => ({
    components: { Button, ArrowLeft: markRaw(ArrowLeft) },
    setup: () => ({ args }),
    template: `
      <div style="width: 24rem">
        <Button v-bind="args"><ArrowLeft :size="14" /> back</Button>
      </div>
    `,
  }),
};
