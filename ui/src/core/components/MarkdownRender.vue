<script setup lang="ts">
import { marked } from 'marked';
import { computed } from 'vue';
import DOMPurify from 'dompurify'

const props = defineProps<{
  code: string;
}>()

const html = computed(() => DOMPurify.sanitize(marked.parse(props.code, { async: false })))

</script>
<template>
  <div :class="$style.md" v-html="html"></div>
</template>
<style module lang="scss">
.md {

  ul,
  ol {
    padding-inline-start: 30px;
  }

  h1,
  h2,
  h3,
  h4,
  p,
  ul,
  ol {
    margin: 1em 0px !important;
  }
}
</style>
