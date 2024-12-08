<script setup lang="ts">
import { RouterView } from 'vue-router';
import { usePageStore } from './core/page-store';
import { storeToRefs } from 'pinia';


const pageStore = usePageStore()
const { confirmations, notifications } = storeToRefs(pageStore);

</script>
<template>
  <RouterView></RouterView>

  <template v-for="item in confirmations" :key="item.id">
    <VDialog :model-value="true" max-width="480px" persistent>
      <VCard>
        <VCardTitle>
          <span class="text-h5">Please confirm this action</span>
        </VCardTitle>
        <VCardText>
          {{ item.question }}
        </VCardText>
        <VCardActions>
          <VCheckbox v-model="item.autoConfirm" label="Auto confirmation for a while" hide-details />
          <VSpacer></VSpacer>
          <VBtn variant="text" @click="pageStore.setConfirmed(item, false)">No</VBtn>
          <VBtn color="blue-darken-1" variant="text" @click="pageStore.setConfirmed(item, true)">Yes</VBtn>
        </VCardActions>
      </VCard>
    </VDialog>
  </template>

  <template v-for="notification in notifications" :key="notification.id">
    <VSnackbar :model-value="true" :color="notification.color">
      {{ notification.message }}
      <template v-slot:actions>
        <VBtn variant="text" @click="pageStore.markNotificationViewed(notification)">Close</VBtn>
      </template>
    </VSnackbar>
  </template>
</template>
