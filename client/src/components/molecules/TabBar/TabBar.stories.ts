import type { Meta, StoryObj } from "@storybook/vue3-vite";
import TabBar from "./TabBar.vue";
import Tab from "./Tab.vue";
import { File, Link } from "lucide-vue-next";
import { ref, markRaw } from "vue";

const meta = {
  title: "Molecules/TabBar",
  component: TabBar,
  tags: ["autodocs"],
} satisfies Meta<typeof TabBar>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => ({
    components: { TabBar, Tab },
    setup() {
      const active = ref("upload");
      const FileIcon = markRaw(File);
      const LinkIcon = markRaw(Link);
      return { active, FileIcon, LinkIcon };
    },
    template: `
      <TabBar v-model="active" style="width: 18.75rem">
        <Tab value="upload" :icon="FileIcon" label="active_tab" />
        <Tab value="url" :icon="LinkIcon" label="inactive_tab" />
      </TabBar>
    `,
  }),
};
