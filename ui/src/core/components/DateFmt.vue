<script setup lang="ts">
import { formatDate, relativeTime } from '@/utils/dates';

const props = defineProps<{
  date: number|Date;
}>()

</script>
<template>
  {{ formatDate(props.date) }}
  <span class="text-disabled ms-1 text-no-wrap">({{ relativeTime(props.date) }})</span>
</template>
