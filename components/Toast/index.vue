<script setup lang="ts">
export interface IToastProps {
  open: boolean;
  variant: "error" | "success" | "info" | "warning";
  title: string;
  description: string;
}

export interface IToastHandler {
  (e: "close"): void;
}

const props = defineProps<IToastProps>();
const emit = defineEmits<IToastHandler>();

const styles = computed(() => {
  switch (props.variant) {
    case "error":
      return "bg-red-500 text-black";
    case "success":
      return "bg-green-500 text-black";
    case "info":
      return "bg-blue-500 text-black";
    case "warning":
      return "bg-yellow-500 text-black";
    default:
      return "";
  }
});

const iconBg = computed(() => {
  switch (props.variant) {
    case "error":
      return "bg-red-300";
    case "success":
      return "bg-green-300";
    case "info":
      return "bg-blue-300";
    case "warning":
      return "bg-yellow-300";
    default:
      return "";
  }
});

const icon = computed(
  () =>
    ({
      error: "uil:dizzy-meh",
      success: "uil:check-circle",
      info: "uil:info-circle",
      warning: "uil:exclamation-circle",
    })[props.variant],
);

const baseStyles = computed(
  () =>
    "border-2 w-[400px] border-black shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] data-[state=open]:animate-slideIn data-[state=closed]:animate-hide data-[swipe=move]:translate-x-[var(--reka-toast-swipe-move-x)] data-[swipe=cancel]:translate-x-0 data-[swipe=cancel]:transition-[transform_200ms_ease-out] data-[swipe=end]:animate-swipeOut",
);

const baseIconStyles = computed(
  () => "w-20 aspect-square flex items-center justify-center border-r-2 border-black",
);
</script>

<template>
  <ToastRoot :open="open" :class="[baseStyles, styles]">
    <div class="flex">
      <div :class="[baseIconStyles, iconBg]">
        <Icon :name="icon" class="size-12 text-black" />
      </div>
      <div class="p-2 w-full">
        <div class="flex w-full justify-between">
          <ToastTitle class="[grid-area:_title] mb-[5px] text-slate12 text-sm font-[700]">
            {{ title }}
          </ToastTitle>
          <ToastClose
            class="[grid-area:_action]"
            as-child
            alt-text="Goto schedule to undo"
            @click="emit('close')"
          >
            <Icon name="uil:times" />
          </ToastClose>
        </div>
        <ToastDescription as-child>
          <p>{{ description }}</p>
        </ToastDescription>
      </div>
    </div>
  </ToastRoot>
  <ToastViewport
    class="[--viewport-padding:_25px] fixed bottom-0 right-16 flex flex-col p-[var(--viewport-padding)] gap-[10px] w-[390px] max-w-[100vw] m-0 list-none z-[2147483647] outline-none"
  />
</template>
