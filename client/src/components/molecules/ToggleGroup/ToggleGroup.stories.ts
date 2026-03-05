import type { Meta, StoryObj } from "@storybook/vue3-vite";
import ToggleGroup from "./ToggleGroup.vue";
import ToggleGroupItem from "./ToggleGroupItem.vue";
import { ref } from "vue";

const meta = {
  title: "Molecules/ToggleGroup",
  component: ToggleGroup,
  tags: ["autodocs"],
} satisfies Meta<typeof ToggleGroup>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => ({
    components: { ToggleGroup, ToggleGroupItem },
    setup() {
      const selected = ref("");
      return { selected };
    },
    template: `
      <ToggleGroup v-model="selected">
        <ToggleGroupItem value="google-drive" label="Google Drive" />
        <ToggleGroupItem value="onedrive" label="OneDrive" />
        <ToggleGroupItem value="dropbox" label="Dropbox" />
      </ToggleGroup>
      <p style="margin-top: 1rem; font-size: 0.75rem">Selected: {{ selected || 'none' }}</p>
    `,
  }),
};
