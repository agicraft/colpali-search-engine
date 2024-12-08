<script setup lang="ts">
import { computed } from 'vue';
import { useInterpretStore } from '../interpret-store';
import { storeToRefs } from 'pinia';
import { useService } from '@/utils/di';
import { ClassifierApiService } from '../ClassifierApiService';
import { VImg } from 'vuetify/components';

const interpretStore = useInterpretStore()
const { chunkId: targetChunkId, query: targetQuery } = storeToRefs(interpretStore)
const service = useService(ClassifierApiService)
const dialogVisible = computed({
  get: () => targetChunkId.value !== null,
  set: (visible) => {
    if (!visible) {
      interpretStore.hide()
    }
  },
})

</script>

<template>
  <VDialog max-width="640" v-model="dialogVisible">
    <VCard title="Интерпретация: карта внимания">
      <VCardText :class="$style.overflow" v-if="targetChunkId && targetQuery">
        <VImg :src="service.getChunkInterpretUrl(targetChunkId, targetQuery)" min-height="200">
          <template v-slot:placeholder>
            <VProgressLinear indeterminate />
          </template>
          <template v-slot:error>
            Ошибка загрузки..
          </template>
        </VImg>
      </VCardText>
      <VCardActions>
        <VSpacer></VSpacer>
        <VBtn text="Закрыть" @click="interpretStore.hide()"></VBtn>
      </VCardActions>
    </VCard>
  </VDialog>
</template>
<style module lang="scss">
.overflow {
  overflow-y: scroll;
  max-height: 500px;
}
</style>
