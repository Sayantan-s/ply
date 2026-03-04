import type { Meta, StoryObj } from "@storybook/vue3-vite";
import MatchReport from "./MatchReport.vue";

const meta = {
  title: "JdMatch/Organisms/MatchReport",
  component: MatchReport,
  tags: ["autodocs"],
} satisfies Meta<typeof MatchReport>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    analysis: {
      score: 78,
      matchingSkills: ["React / Next.js", "TypeScript", "System Design"],
      missingSkills: ["Backend Infrastructure", "Team Leadership"],
      explanation:
        "Strong alignment in frontend technologies and system design. Key gaps exist in backend infrastructure experience and years of leadership.",
    },
  },
};

export const HighScore: Story = {
  args: {
    analysis: {
      score: 95,
      matchingSkills: ["React", "TypeScript", "Node.js", "System Design", "CI/CD"],
      missingSkills: [],
      explanation:
        "Excellent match across all key areas. The candidate meets or exceeds all listed requirements.",
    },
  },
};

export const LowScore: Story = {
  args: {
    analysis: {
      score: 32,
      matchingSkills: ["JavaScript"],
      missingSkills: ["React", "TypeScript", "Node.js", "AWS", "Docker"],
      explanation:
        "Significant gaps in most required skills. The candidate's experience does not align well with this role.",
    },
  },
};
