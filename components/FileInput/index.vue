<script setup lang="ts">
interface IProps {
  file: File | null;
  inputParentClassName?: string;
}

const props = defineProps<IProps>();

const emit = defineEmits<{
  (e: "change", file: File | null): Promise<void>;
}>();

const fileRef = ref<HTMLInputElement | null>(null);

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) emit("change", target.files[0]);
};

const handleRemoveFile = () => {
  if (props.file) emit("change", null);
};

const handleTriggerFile = (eve: Event) => {
  eve.preventDefault();
  eve.stopPropagation();
  if (fileRef.value) fileRef.value.click();
};
</script>

<template>
  <div :class="inputParentClassName">
    <input ref="fileRef" type="file" hidden v-bind="$attrs" @input="handleFileChange" />
    <slot :trigger="handleTriggerFile" :remove="handleRemoveFile" />
  </div>
</template>

<style></style>
