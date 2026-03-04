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
  gap: 0.625rem;
  padding: 0.625rem 0;
  width: 100%;
  border-bottom: 1px solid #E8E8EC;
}

.skill-item__icon {
  width: 1rem;
  height: 1rem;
  flex-shrink: 0;
}

.skill-item--match .skill-item__icon { color: var(--success); }
.skill-item--missing .skill-item__icon { color: var(--error); }

.skill-item__skill {
  font-family: var(--font);
  font-size: 0.75rem;
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
  font-size: 0.5625rem;
  font-weight: 600;
  color: var(--success);
  background: var(--success-bg);
  padding: 0.125rem 0.5rem;
}

.skill-item__content {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  flex: 1;
}

.skill-item__detail {
  font-family: var(--font);
  font-size: 0.625rem;
  font-weight: 400;
  color: var(--muted);
}
</style>
