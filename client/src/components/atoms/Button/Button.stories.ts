import type { Meta, StoryObj } from "@storybook/vue3-vite";
import Button from "./Button.vue";
import ButtonLoading from "./ButtonLoading.vue";
import ButtonIcon from "./ButtonIcon.vue";
import ButtonContent from "./ButtonContent.vue";
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
    components: { Button, ButtonContent, ButtonIcon },
    setup: () => ({ args, ArrowRight: markRaw(ArrowRight) }),
    template: '<Button v-bind="args"><ButtonContent>next: job_description</ButtonContent><ButtonIcon :icon="ArrowRight" position="post" :size="16" /></Button>',
  }),
};

export const Accent: Story = {
  args: { variant: "accent" },
  render: (args) => ({
    components: { Button, ButtonContent, ButtonIcon },
    setup: () => ({ args, Sparkles: markRaw(Sparkles) }),
    template: '<Button v-bind="args"><ButtonIcon :icon="Sparkles" position="pre" :size="18" /><ButtonContent>run_match_report</ButtonContent></Button>',
  }),
};

export const Outline: Story = {
  args: { variant: "outline" },
  render: (args) => ({
    components: { Button, ButtonContent, ButtonIcon },
    setup: () => ({ args, Download: markRaw(Download) }),
    template: '<Button v-bind="args"><ButtonIcon :icon="Download" position="pre" :size="14" /><ButtonContent>download</ButtonContent></Button>',
  }),
};

export const Ghost: Story = {
  args: { variant: "ghost" },
  render: (args) => ({
    components: { Button, ButtonContent },
    setup: () => ({ args }),
    template: '<Button v-bind="args"><ButtonContent>go_back</ButtonContent></Button>',
  }),
};

export const Fluid: Story = {
  args: { variant: "primary", fluid: true },
  render: (args) => ({
    components: { Button, ButtonContent, ButtonIcon },
    setup: () => ({ args, ArrowRight: markRaw(ArrowRight) }),
    template: `
      <div style="width: 24rem">
        <Button v-bind="args"><ButtonContent>next: job_description</ButtonContent><ButtonIcon :icon="ArrowRight" position="post" :size="16" /></Button>
      </div>
    `,
  }),
};

export const Loading: Story = {
  args: { variant: "accent", loading: true, fluid: true },
  render: (args) => ({
    components: { Button, ButtonLoading, ButtonIcon, ButtonContent },
    setup: () => ({ args, Sparkles: markRaw(Sparkles) }),
    template: `
      <div style="width: 24rem">
        <Button v-bind="args">
          <ButtonLoading>analyzing...</ButtonLoading>
          <ButtonIcon :icon="Sparkles" position="pre" :size="18" />
          <ButtonContent>run_match_report</ButtonContent>
        </Button>
      </div>
    `,
  }),
};

export const LoadingGrid: Story = {
  args: { variant: "primary", loading: true, fluid: true },
  render: (args) => ({
    components: { Button, ButtonLoading, ButtonIcon, ButtonContent },
    setup: () => ({ args, Sparkles: markRaw(Sparkles) }),
    template: `
      <div style="width: 24rem">
        <Button v-bind="args">
          <ButtonLoading variant="grid">analyzing...</ButtonLoading>
          <ButtonIcon :icon="Sparkles" position="pre" :size="18" />
          <ButtonContent>run_match_report</ButtonContent>
        </Button>
      </div>
    `,
  }),
};

export const Disabled: Story = {
  args: { variant: "primary", disabled: true, fluid: true },
  render: (args) => ({
    components: { Button, ButtonContent, ButtonIcon },
    setup: () => ({ args, ArrowRight: markRaw(ArrowRight) }),
    template: `
      <div style="width: 24rem">
        <Button v-bind="args"><ButtonContent>next: job_description</ButtonContent><ButtonIcon :icon="ArrowRight" position="post" :size="16" /></Button>
      </div>
    `,
  }),
};

export const BackOutline: Story = {
  args: { variant: "outline", fluid: true },
  render: (args) => ({
    components: { Button, ButtonContent, ButtonIcon },
    setup: () => ({ args, ArrowLeft: markRaw(ArrowLeft) }),
    template: `
      <div style="width: 24rem">
        <Button v-bind="args"><ButtonIcon :icon="ArrowLeft" position="pre" :size="14" /><ButtonContent>back</ButtonContent></Button>
      </div>
    `,
  }),
};
