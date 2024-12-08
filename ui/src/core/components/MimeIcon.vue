<script setup lang="ts">
import { mimeToIcon } from '@/utils/mime-icons';

const props = defineProps<{
  mime: string;
  size?: number;
}>()

const { icon, color } = mimeToIcon(props.mime)

</script>
<template>
  <VIcon :size="props.size" :icon="icon" :style="{ color }" />
</template>
