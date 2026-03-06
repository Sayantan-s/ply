import type { Meta, StoryObj } from "@storybook/vue3-vite";
import Dropzone from "./Dropzone.vue";
import DropzoneEmpty from "./DropzoneEmpty.vue";
import DropzoneFileList from "./DropzoneFileList.vue";

const meta = {
  title: "Molecules/Dropzone",
  component: Dropzone,
  tags: ["autodocs"],
  argTypes: {
    multiple: { control: "boolean" },
    disabled: { control: "boolean" },
    maxSize: { control: { type: "number", min: 1, max: 100 } },
  },
} satisfies Meta<typeof Dropzone>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
  render: (args) => ({
    components: { Dropzone, DropzoneEmpty, DropzoneFileList },
    setup: () => ({ args }),
    template: `
      <Dropzone v-bind="args">
        <DropzoneFileList />
        <DropzoneEmpty />
      </Dropzone>
    `,
  }),
};

export const PdfOnly: Story = {
  args: {
    formats: [".pdf"],
    maxSize: 5,
  },
  render: (args) => ({
    components: { Dropzone, DropzoneEmpty, DropzoneFileList },
    setup: () => ({ args }),
    template: `
      <Dropzone v-bind="args">
        <DropzoneFileList />
        <DropzoneEmpty />
      </Dropzone>
    `,
  }),
};

export const Multiple: Story = {
  args: {
    multiple: true,
    formats: [".pdf", ".docx", ".txt"],
    maxSize: 20,
  },
  render: (args) => ({
    components: { Dropzone, DropzoneEmpty, DropzoneFileList },
    setup: () => ({ args }),
    template: `
      <Dropzone v-bind="args">
        <DropzoneFileList />
        <DropzoneEmpty />
      </Dropzone>
    `,
  }),
};

export const Disabled: Story = {
  args: {
    disabled: true,
  },
  render: (args) => ({
    components: { Dropzone, DropzoneEmpty, DropzoneFileList },
    setup: () => ({ args }),
    template: `
      <Dropzone v-bind="args">
        <DropzoneFileList />
        <DropzoneEmpty />
      </Dropzone>
    `,
  }),
};
