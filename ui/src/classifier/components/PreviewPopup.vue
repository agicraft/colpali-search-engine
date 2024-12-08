<script setup lang="ts">
import { computed, nextTick, ref, useTemplateRef, watch, type ComponentPublicInstance } from 'vue';
import { usePreviewStore } from '../preview-store';
import { storeToRefs } from 'pinia';
import { useService } from '@/utils/di';
import { ClassifierApiService } from '../ClassifierApiService';
import type { DocPreviewDto } from '../classifier-dto';
import { usePageStore } from '@/core/page-store';
import { VImg } from 'vuetify/components';

const previewStore = usePreviewStore()
const pageStore = usePageStore()
const { docId: targetDocId, pageId: targetPageId } = storeToRefs(previewStore)
const service = useService(ClassifierApiService)
const docPreview = ref<DocPreviewDto>()
const loading = ref(0)
const dialogVisible = computed({
  get: () => targetDocId.value !== null,
  set: (visible) => {
    if (!visible) {
      previewStore.hide()
    }
  },
})

const loadDocPreview = async (id: number) => {
  try {
    loading.value++
    const res = await service.previewDocument(id)
    if (id === targetDocId.value) {
      docPreview.value = res
    }
  } catch (e) {
    pageStore.notifyException(e)
  } finally {
    loading.value--
  }
}

const onImageLoad = async (pageId: number) => {
  if (pageId !== targetPageId.value) {
    return;
  }
  if (!imgRefs.value) {
    return;
  }
  // scroll into to view page for corresponding page
  for (const img of imgRefs.value as ComponentPublicInstance[]) {
    if (!img) {
      continue
    }
    if (img.$.vnode.key === pageId) {
      await nextTick()
      img.$el.scrollIntoView()
    }
  }
}

const imgRefs = useTemplateRef('imgs')

watch(targetDocId, async (newVal) => {
  // delete old one first
  docPreview.value = undefined
  if (newVal) {
    await loadDocPreview(newVal)
  }
})

</script>

<template>
  <VDialog max-width="640" v-model="dialogVisible">
    <VCard :title="docPreview?.name" :loading="loading > 0">
      <VCardText :class="$style.overflow">
        <VImg ref="imgs" v-for="pageId in docPreview?.pages" :key="pageId" :src="service.getPageImageUrl(pageId)"
          class="mb-3" @load="onImageLoad(pageId)" />
      </VCardText>
      <VCardActions>
        <VSpacer></VSpacer>
        <VBtn text="Закрыть" @click="previewStore.hide()"></VBtn>
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
