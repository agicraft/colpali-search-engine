<script setup lang="ts">
import { computed, ref } from 'vue';
import { useService } from '@/utils/di';
import { ClassifierApiService } from '../ClassifierApiService';
import type { DocPreviewDto } from '../classifier-dto';
import { usePageStore } from '@/core/page-store';
import MarkdownRender from '@/core/components/MarkdownRender.vue';

const props = defineProps<{
  query: string;
  chunks: number[];
}>()

const pageStore = usePageStore()
const service = useService(ClassifierApiService)
const docPreview = ref<DocPreviewDto>()
const loading = ref(0)
const searchAnswerMd = ref()
let requestId = 0;

const update = async () => {
  loading.value++
  searchAnswerMd.value = undefined
  try {
    if (disabledUpdate.value) {
      return
    }
    requestId++
    const res = await service.ragRequest({ query: props.query, chunks: props.chunks, requestId })
    if (requestId === res.requestId) {
      searchAnswerMd.value = res.answer
    }
  } catch (e) {
    pageStore.notifyException(e)
  } finally {
    loading.value--
  }
}

const disabledUpdate = computed(() => !props.query || !props.chunks.length)

defineExpose({
  update
})

</script>

<template>
  <VCard :title="docPreview?.name" :loading="loading > 0">
    <VCardText v-if="searchAnswerMd">
      <MarkdownRender :code="searchAnswerMd" />
    </VCardText>
    <VCardActions>
      <VSpacer></VSpacer>
      <VBtn text="Обновить ответ" @click="update" :disabled="disabledUpdate"></VBtn>
    </VCardActions>
  </VCard>
</template>
