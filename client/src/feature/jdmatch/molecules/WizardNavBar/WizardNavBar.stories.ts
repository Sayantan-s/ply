import type { Meta, StoryObj } from "@storybook/vue3-vite";
import WizardNavBar from "./WizardNavBar.vue";

const meta = {
  title: "JdMatch/Molecules/WizardNavBar",
  component: WizardNavBar,
  tags: ["autodocs"],
  decorators: [
    () => ({
      template:
        '<div style="width: 1280px; max-width: 100%;"><story /></div>',
    }),
  ],
} satisfies Meta<typeof WizardNavBar>;

export default meta;
type Story = StoryObj<typeof meta>;

export const WizardStep1: Story = {
  args: { variant: "wizard", activeStep: 1 },
};

export const WizardStep2: Story = {
  args: { variant: "wizard", activeStep: 2 },
};

export const WizardStep3: Story = {
  args: { variant: "wizard", activeStep: 3 },
};

export const Report: Story = {
  args: { variant: "report", navTitle: "match_report" },
};

export const Empty: Story = {
  args: { variant: "empty", navTitle: "no_results" },
};
