import type { Meta, StoryObj } from "@storybook/vue3-vite";
import StreamingMatchReport from "./StreamingMatchReport.vue";
import StreamingReportStatus from "./StreamingReportStatus.vue";
import StreamingReportScore from "./StreamingReportScore.vue";
import StreamingReportSummary from "./StreamingReportSummary.vue";
import StreamingReportSkills from "./StreamingReportSkills.vue";

const meta = {
  title: "JdMatch/Organisms/StreamingMatchReport",
  component: StreamingMatchReport,
  tags: ["autodocs"],
  decorators: [
    () => ({
      template:
        '<div style="width: 880px; max-width: 100%; padding: 2.5rem;"><story /></div>',
    }),
  ],
  argTypes: {
    variant: {
      control: "select",
      options: ["default", "compact"],
    },
    score: { control: { type: "number", min: 0, max: 100 } },
    isExplanationStreaming: { control: "boolean" },
    currentStatus: {
      control: "select",
      options: [
        "warming_up",
        "lining_up",
        "churning",
        "combing",
        "pondering",
        "cooking",
        "locked_in",
        "fumbled",
      ],
    },
  },
} satisfies Meta<typeof StreamingMatchReport>;

export default meta;
type Story = StoryObj<typeof meta>;

const streamingTemplate = `
  <StreamingMatchReport v-bind="args">
    <StreamingReportStatus />
    <div style="display: flex; gap: 2.5rem; width: 100%;">
      <div style="display: flex; flex-direction: column; gap: 1.75rem; flex: 0.5; background-color: var(--bg); padding: 1.25rem; height: max-content;">
        <StreamingReportScore />
        <StreamingReportSummary />
      </div>
      <div style="display: flex; flex-direction: column; gap: 1.75rem; flex: 0.5; overflow: auto; padding: 1.25rem;">
        <StreamingReportSkills />
      </div>
    </div>
  </StreamingMatchReport>
`;

const storyComponents = {
  StreamingMatchReport,
  StreamingReportStatus,
  StreamingReportScore,
  StreamingReportSummary,
  StreamingReportSkills,
};

export const Loading: Story = {
  args: {
    score: null,
    matchingSkills: null,
    missingSkills: null,
    streamedExplanation: "",
    isExplanationStreaming: false,
    currentStatus: "warming_up",
  },
  render: (args) => ({
    components: storyComponents,
    setup: () => ({ args }),
    template: streamingTemplate,
  }),
};

export const StreamingExplanation: Story = {
  args: {
    score: 78,
    matchingSkills: ["React / Next.js", "TypeScript", "System Design"],
    missingSkills: ["Backend Infrastructure", "Team Leadership"],
    streamedExplanation:
      "Strong alignment in frontend technologies and system design. Key gaps exist in...",
    isExplanationStreaming: true,
    currentStatus: "churning",
  },
  render: (args) => ({
    components: storyComponents,
    setup: () => ({ args }),
    template: streamingTemplate,
  }),
};

export const Complete: Story = {
  args: {
    score: 78,
    matchingSkills: ["React / Next.js", "TypeScript", "System Design"],
    missingSkills: ["Backend Infrastructure", "Team Leadership"],
    streamedExplanation:
      "Strong alignment in frontend technologies and system design. Key gaps exist in backend infrastructure experience and years of leadership.",
    isExplanationStreaming: false,
    currentStatus: "locked_in",
  },
  render: (args) => ({
    components: storyComponents,
    setup: () => ({ args }),
    template: streamingTemplate,
  }),
};

export const HighScore: Story = {
  args: {
    score: 95,
    matchingSkills: [
      "React",
      "TypeScript",
      "Node.js",
      "System Design",
      "CI/CD",
    ],
    missingSkills: [],
    streamedExplanation:
      "Excellent match across all key areas. The candidate meets or exceeds all listed requirements.",
    isExplanationStreaming: false,
    currentStatus: "locked_in",
  },
  render: (args) => ({
    components: storyComponents,
    setup: () => ({ args }),
    template: streamingTemplate,
  }),
};

export const LowScore: Story = {
  args: {
    score: 32,
    matchingSkills: ["JavaScript"],
    missingSkills: ["React", "TypeScript", "Node.js", "AWS", "Docker"],
    streamedExplanation: "Significant gaps in most required skills.",
    isExplanationStreaming: false,
    currentStatus: "locked_in",
  },
  render: (args) => ({
    components: storyComponents,
    setup: () => ({ args }),
    template: streamingTemplate,
  }),
};

export const Compact: Story = {
  args: {
    score: 78,
    matchingSkills: ["React / Next.js", "TypeScript", "System Design"],
    missingSkills: ["Backend Infrastructure", "Team Leadership"],
    streamedExplanation:
      "Strong alignment in frontend technologies and system design. Key gaps exist in backend infrastructure experience and years of leadership.",
    isExplanationStreaming: false,
    currentStatus: "locked_in",
    variant: "compact",
  },
  render: (args) => ({
    components: storyComponents,
    setup: () => ({ args }),
    template: streamingTemplate,
  }),
};

export const Error: Story = {
  args: {
    score: null,
    matchingSkills: null,
    missingSkills: null,
    streamedExplanation: "",
    isExplanationStreaming: false,
    currentStatus: "fumbled",
  },
  render: (args) => ({
    components: storyComponents,
    setup: () => ({ args }),
    template: streamingTemplate,
  }),
};
