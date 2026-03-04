import type { Meta, StoryObj } from "@storybook/vue3-vite";
import StepLayout from "./StepLayout.vue";

const meta = {
  title: "JdMatch/Templates/StepLayout",
  component: StepLayout,
  tags: ["autodocs"],
} satisfies Meta<typeof StepLayout>;

export default meta;
type Story = StoryObj<typeof meta>;

export const WithStep: Story = {
  args: { stepLabel: "01/03" },
  render: (args) => ({
    components: { StepLayout },
    setup: () => ({ args }),
    template: `
      <StepLayout v-bind="args">
        <div style="padding: 2rem; background: var(--surface); text-align: center; font-family: var(--font); font-size: 0.75rem; color: var(--muted);">
          Content area
        </div>
        <template #footer>
          <div style="padding: 1rem; background: var(--surface); text-align: center; font-family: var(--font); font-size: 0.75rem; color: var(--muted);">
            Footer area
          </div>
        </template>
      </StepLayout>
    `,
  }),
};

export const NoStep: Story = {
  args: { stepLabel: null },
  render: (args) => ({
    components: { StepLayout },
    setup: () => ({ args }),
    template: `
      <StepLayout v-bind="args">
        <div style="padding: 2rem; background: var(--surface); text-align: center; font-family: var(--font); font-size: 0.75rem; color: var(--muted);">
          Content without step indicator
        </div>
      </StepLayout>
    `,
  }),
};
