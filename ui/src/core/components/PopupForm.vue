<script setup lang="ts">
import { VDialog } from 'vuetify/components'
import { ref } from 'vue';
import { useDisplay } from 'vuetify'

const { mobile } = useDisplay()

const dialogVisibility = ref(false);
let resolveCb: ((success: boolean) => void) | undefined;

const doResolve = (success: boolean) => {
  dialogVisibility.value = false;
  if (resolveCb) {
    resolveCb(success);
    resolveCb = undefined;
  }
}

const close = () => doResolve(false);
const submit = () => doResolve(true);

const show = () => {
  dialogVisibility.value = true;
  return new Promise((resolve: (success: boolean) => void) => {
    resolveCb = resolve;
  })
}

defineExpose({ show })

</script>
<template>
  <VDialog v-model="dialogVisibility" :fullscreen="mobile" max-width="480px" persistent>
    <slot v-if="dialogVisibility" :submit="submit" :close="close"></slot>
  </VDialog>
</template>
