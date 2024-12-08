<script setup lang="ts">
import { mdiMagnify } from '@mdi/js';
import { VCol, VContainer, VRow, VForm, VTextField } from 'vuetify/components';
import { useRouter } from 'vue-router';
import { linkFactory } from '@/router';
import { computed, ref } from 'vue';
import BrandWide from '@/components/BrandWide.vue';
import AppHeader from '@/components/AppHeader.vue';

const router = useRouter();

const searchQuery = ref('')

const allowSubmit = computed(() => !!searchQuery.value)

const onSubmit = () => {
  if (!allowSubmit.value) {
    return
  }
  router.push(linkFactory.toSearchResults(searchQuery.value))
}

</script>

<template>
  <VContainer class="flex-1-1 d-flex flex-column position-relative">
    <div class="position-absolute d-flex justify-end ga-4 right-0 px-4">
      <AppHeader/>
    </div>
    <VRow class="flex-1-1 align-center justify-center">
      <VCol cols="12" sm="10" md="8" lg="6" xl="4" class="d-flex">
        <VForm @submit.prevent="onSubmit" class="flex-1-1">
          <h1 class="text-center mb-3">
            <BrandWide />
          </h1>
          <div class="mb-5">
            <VTextField v-model="searchQuery" :prepend-inner-icon="mdiMagnify" variant="outlined" hide-details />
          </div>
          <div class="d-flex justify-center">
            <VBtn type="submit" :disabled="!allowSubmit">Начать поиск</VBtn>
          </div>
        </VForm>
      </VCol>
    </VRow>
  </VContainer>
</template>
