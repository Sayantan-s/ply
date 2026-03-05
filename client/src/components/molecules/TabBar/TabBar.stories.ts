import type { Meta, StoryObj } from "@storybook/vue3-vite";
import TabBar from "./TabBar.vue";
import Tab from "./Tab.vue";
import TabContent from "./TabContent.vue";
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
    components: { TabBar, Tab, TabContent },
    setup() {
      const active = ref("upload");
      const FileIcon = markRaw(File);
      const LinkIcon = markRaw(Link);
      return { active, FileIcon, LinkIcon };
    },
    template: `
      <TabBar v-model="active" style="width: 18.75rem">
        <template #triggers>
          <Tab value="upload" :icon="FileIcon" label="File Upload" />
          <Tab value="url" :icon="LinkIcon" label="Cloud Link" />
        </template>
        <TabContent value="upload">
          <p style="padding: 1rem">Upload panel content</p>
        </TabContent>
        <TabContent value="url">
          <p style="padding: 1rem">URL panel content</p>
        </TabContent>
      </TabBar>
    `,
  }),
};

export const WithDisabledTab: Story = {
  render: () => ({
    components: { TabBar, Tab, TabContent },
    setup() {
      const active = ref("upload");
      const FileIcon = markRaw(File);
      const LinkIcon = markRaw(Link);
      return { active, FileIcon, LinkIcon };
    },
    template: `
      <TabBar v-model="active" style="width: 18.75rem">
        <template #triggers>
          <Tab value="upload" :icon="FileIcon" label="File Upload" />
          <Tab value="url" :icon="LinkIcon" label="Cloud Link" disabled />
        </template>
        <TabContent value="upload">
          <p style="padding: 1rem">Upload panel content</p>
        </TabContent>
        <TabContent value="url">
          <p style="padding: 1rem">URL panel content (disabled)</p>
        </TabContent>
      </TabBar>
    `,
  }),
};
