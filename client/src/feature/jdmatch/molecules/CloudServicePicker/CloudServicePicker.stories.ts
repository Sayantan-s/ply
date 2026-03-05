import type { Meta, StoryObj } from "@storybook/vue3-vite";
import CloudServicePicker from "./CloudServicePicker.vue";
import { ref } from "vue";

const meta = {
  title: "JdMatch/Molecules/CloudServicePicker",
  component: CloudServicePicker,
  tags: ["autodocs"],
} satisfies Meta<typeof CloudServicePicker>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => ({
    components: { CloudServicePicker },
    setup() {
      const selected = ref("");
      return { selected };
    },
    template: `
      <CloudServicePicker v-model="selected" />
      <p style="margin-top: 1rem; font-size: 0.75rem">Selected: {{ selected || 'none' }}</p>
    `,
  }),
};
