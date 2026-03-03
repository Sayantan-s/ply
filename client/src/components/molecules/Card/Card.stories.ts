import type { Meta, StoryObj } from "@storybook/vue3-vite";
import Card from "./Card.vue";
import CardHeader from "./CardHeader.vue";
import CardBody from "./CardBody.vue";
import { FileText } from "lucide-vue-next";
import { markRaw } from "vue";

const meta = {
  title: "Molecules/Card",
  component: Card,
  tags: ["autodocs"],
} satisfies Meta<typeof Card>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => ({
    components: { Card, CardHeader, CardBody },
    setup() {
      const FileTextIcon = markRaw(FileText);
      return { FileTextIcon };
    },
    template: `
      <Card>
        <CardHeader :icon="FileTextIcon" title="card_title" />
        <CardBody>
          Card body content goes here. Supports multi-line text wrapping.
        </CardBody>
      </Card>
    `,
  }),
};
