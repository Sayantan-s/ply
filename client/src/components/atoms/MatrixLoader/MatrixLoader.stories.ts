import type { Meta, StoryObj } from "@storybook/vue3-vite";
import MatrixLoader from "./MatrixLoader.vue";

const meta = {
  title: "Atoms/MatrixLoader",
  component: MatrixLoader,
  tags: ["autodocs"],
  argTypes: {
    variant: {
      control: "select",
      options: ["text", "grid"],
    },
    size: {
      control: "select",
      options: ["sm", "md", "lg"],
    },
    tone: {
      control: "select",
      options: ["inherit", "accent", "success", "muted"],
    },
    cols: { control: { type: "number", min: 2, max: 12 } },
  },
} satisfies Meta<typeof MatrixLoader>;

export default meta;
type Story = StoryObj<typeof meta>;

/* ── Text variant ── */

export const Default: Story = {
  args: {},
};

export const Medium: Story = {
  args: { size: "md", cols: 7 },
};

export const Large: Story = {
  args: { size: "lg", cols: 8 },
};

export const Accent: Story = {
  args: { size: "md", tone: "accent", cols: 6 },
};

export const Success: Story = {
  args: { size: "md", tone: "success", cols: 6 },
};

export const Muted: Story = {
  args: { size: "sm", tone: "muted", cols: 4 },
};

export const InButton: Story = {
  render: (args) => ({
    components: { MatrixLoader },
    setup: () => ({ args }),
    template: `
      <button style="
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        height: 3rem;
        padding: 0 1.5rem;
        background: #1A1B2E;
        color: #fff;
        border: none;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8125rem;
        font-weight: 600;
        cursor: pointer;
      ">
        <MatrixLoader v-bind="args" />
        analyzing...
      </button>
    `,
  }),
  args: { size: "sm", cols: 3 },
};

/* ── Grid variant ── */

export const GridSmall: Story = {
  args: { variant: "grid", size: "sm" },
};

export const GridMedium: Story = {
  args: { variant: "grid", size: "md" },
};

export const GridLarge: Story = {
  args: { variant: "grid", size: "lg" },
};

export const GridAccent: Story = {
  args: { variant: "grid", size: "md", tone: "accent" },
};

export const GridMuted: Story = {
  args: { variant: "grid", size: "md", tone: "muted" },
};

export const GridInButton: Story = {
  render: (args) => ({
    components: { MatrixLoader },
    setup: () => ({ args }),
    template: `
      <button style="
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        height: 3rem;
        padding: 0 1.5rem;
        background: #1A1B2E;
        color: #fff;
        border: none;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8125rem;
        font-weight: 600;
        cursor: pointer;
      ">
        <MatrixLoader v-bind="args" />
        analyzing...
      </button>
    `,
  }),
  args: { size: "sm", variant: "grid" },
};
