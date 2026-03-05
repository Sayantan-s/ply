import type { Meta, StoryObj } from "@storybook/vue3-vite";
import StepLayout from "./StepLayout.vue";

const meta = {
  title: "JdMatch/Templates/StepLayout",
  component: StepLayout,
  tags: ["autodocs"],
  decorators: [
    () => ({
      template:
        '<div style="width: 1280px; max-width: 100%; min-height: 600px;"><story /></div>',
    }),
  ],
} satisfies Meta<typeof StepLayout>;

export default meta;
type Story = StoryObj<typeof meta>;

export const WizardStep1: Story = {
  args: { navVariant: "wizard", activeStep: 1 },
  render: (args) => ({
    components: { StepLayout },
    setup: () => ({ args }),
    template: `
      <StepLayout v-bind="args">
        <div style="padding: 2rem; text-align: center; font-family: var(--font); font-size: 0.75rem; color: var(--muted);">
          Step 1 content area
        </div>
      </StepLayout>
    `,
  }),
};

export const ReportLayout: Story = {
  args: { navVariant: "report", noCard: true },
  render: (args) => ({
    components: { StepLayout },
    setup: () => ({ args }),
    template: `
      <StepLayout v-bind="args">
        <div style="padding: 2rem; text-align: center; font-family: var(--font); font-size: 0.75rem; color: var(--muted);">
          Two-column report content
        </div>
      </StepLayout>
    `,
  }),
};

export const ErrorLayout: Story = {
  args: { navVariant: "wizard", activeStep: 1, cardWidth: 480 },
  render: (args) => ({
    components: { StepLayout },
    setup: () => ({ args }),
    template: `
      <StepLayout v-bind="args">
        <div style="padding: 2rem; text-align: center; font-family: var(--font); font-size: 0.75rem; color: var(--muted);">
          Error state content (480px card)
        </div>
      </StepLayout>
    `,
  }),
};
