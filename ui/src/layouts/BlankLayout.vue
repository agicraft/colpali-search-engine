<script setup lang="ts">
import LoaderWrapper from '@/core/components/LoaderWrapper.vue';
import { RouterView } from 'vue-router';
import { VApp } from 'vuetify/components';
</script>
<template>
  <VApp>
    <LoaderWrapper />
    <RouterView />
  </VApp>
</template>
