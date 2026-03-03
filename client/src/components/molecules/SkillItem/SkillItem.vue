<script setup lang="ts">
import { computed } from "vue";
import { cva, type VariantProps } from "class-variance-authority";
import { Check, X } from "lucide-vue-next";

const skillItemVariants = cva("skill-item", {
  variants: {
    variant: {
      match: "skill-item--match",
      missing: "skill-item--missing",
    },
  },
  defaultVariants: { variant: "match" },
});

type SkillItemVariants = VariantProps<typeof skillItemVariants>;

const props = defineProps<{
  variant?: NonNullable<SkillItemVariants["variant"]>;
  skill: string;
  badge?: string;
  detail?: string;
}>();

const classes = computed(() => skillItemVariants({ variant: props.variant }));
const iconComponent = computed(() => (props.variant === "missing" ? X : Check));
</script>

<template>
  <div :class="classes">
    <component :is="iconComponent" class="skill-item__icon" />

    <template v-if="variant === 'missing'">
      <div class="skill-item__content">
        <span class="skill-item__skill skill-item__skill--bold">{{ skill }}</span>
        <span v-if="detail" class="skill-item__detail">{{ detail }}</span>
      </div>
    </template>

    <template v-else>
      <span class="skill-item__skill">{{ skill }}</span>
      <span class="skill-item__spacer" />
      <span v-if="badge" class="skill-item__badge">{{ badge }}</span>
    </template>
  </div>
</template>

<style scoped>
.skill-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
  width: 300px;
  border-bottom: 1px solid #E8E8EC;
}

.skill-item__icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.skill-item--match .skill-item__icon { color: var(--success); }
.skill-item--missing .skill-item__icon { color: var(--error); }

.skill-item__skill {
  font-family: var(--font);
  font-size: 12px;
  font-weight: 400;
  color: var(--fg);
}

.skill-item__skill--bold {
  font-weight: 600;
}

.skill-item__spacer {
  flex: 1;
}

.skill-item__badge {
  font-family: var(--font);
  font-size: 9px;
  font-weight: 600;
  color: var(--success);
  background: var(--success-bg);
  padding: 2px 8px;
}

.skill-item__content {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}

.skill-item__detail {
  font-family: var(--font);
  font-size: 10px;
  font-weight: 400;
  color: var(--muted);
}
</style>
