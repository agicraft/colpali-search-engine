<script setup lang="ts">
import { mdiDownload, mdiEye, mdiSearchWeb } from '@mdi/js';
import { VBtn, VCard, VCardText, VCol, VContainer, VForm, VImg, VRow, VSpacer, VTextField } from 'vuetify/components';
import { useRoute } from 'vue-router';
import { computed, nextTick, onBeforeMount, ref } from 'vue';
import BrandWide from '@/components/BrandWide.vue';
import { linkFactory } from '@/router';
import { usePageStore } from '@/core/page-store';
import { useService } from '@/utils/di';
import { ClassifierApiService } from '../ClassifierApiService';
import type { SearchDocumentDto } from '../classifier-dto';
import MimeIcon from '@/core/components/MimeIcon.vue';
import DateFmt from '@/core/components/DateFmt.vue';
import AppHeader from '@/components/AppHeader.vue';
import PreviewPopup from '../components/PreviewPopup.vue';
import { usePreviewStore } from '../preview-store';
import RagAnswer from '../components/RagAnswer.vue';
import { useInterpretStore } from '../interpret-store';
import InterpretPopup from '../components/InterpretPopup.vue';

const route = useRoute()
const pageStore = usePageStore()
const previewStore = usePreviewStore()
const interpretStore = useInterpretStore()
const service = useService(ClassifierApiService)


const searchQuery = ref('')
const lastSearchQuery = ref('')
const searchDocuments = ref<SearchDocumentDto[]>([])
const hasAnswer = ref(false)

const ragChunks = computed(() => (searchDocuments.value.map(({ chunkId }) => chunkId)))
const rag = ref<InstanceType<typeof RagAnswer>>()


const updateSearch = async () => {
  if (!searchQuery.value) {
    return
  }
  try {
    pageStore.isLoading = true
    lastSearchQuery.value = searchQuery.value
    const result = await service.search(searchQuery.value)
    searchDocuments.value = result.documents;
    hasAnswer.value = true;
    await nextTick()
    if (rag.value) {
      await rag.value.update()
    }
  } catch (e) {
    pageStore.notifyException(e)
  } finally {
    pageStore.isLoading = false
  }
}

const excludeChunk = (exclChunkId: number) => {
  searchDocuments.value = searchDocuments.value.filter(({ chunkId }) => chunkId !== exclChunkId)
}

onBeforeMount(async () => {
  const query = String(route.query.q)
  if (query) {
    searchQuery.value = query
    await updateSearch()
  }
})

</script>

<template>
  <PreviewPopup />
  <InterpretPopup />
  <VContainer>
    <VRow no-gutters justify="center">
      <VCol cols="12" md="11" lg="8" xl="6">
        <AppHeader class="mb-4" />
        <VRow>
          <VCol class="d-flex ga-5 flex-column justify-sm-center align-sm-center flex-sm-row">
            <RouterLink :to="linkFactory.toHome()" class="text-decoration-none">
              <h1 class="text-center">
                <BrandWide />
              </h1>
            </RouterLink>
            <VForm class="d-flex flex-1-1" @submit.prevent="updateSearch">
              <VTextField class="flex-1-1" v-model="searchQuery" :append-inner-icon="mdiSearchWeb"
                @click:append-inner="updateSearch" variant="outlined" hide-details />
            </VForm>
          </VCol>
        </VRow>
        <template v-if="hasAnswer">
          <VRow>
            <VCol>
              <h2 class="mt-4 text-secondary">Ответ от ИИ</h2>
            </VCol>
          </VRow>
          <VRow>
            <VCol>
              <RagAnswer ref="rag" :chunks="ragChunks" :query="searchQuery" />
            </VCol>
          </VRow>
          <VRow>
            <VCol>
              <h2 class="mt-4 text-secondary">
                <template v-if="searchDocuments.length > 0">Результаты поиска</template>
                <template v-else>Ничего не найдено</template>
              </h2>
            </VCol>
          </VRow>
          <VRow>
            <VCol cols="12" md="6" v-for="doc in searchDocuments" :key="doc.chunkId">
              <VCard elevation="4" min-width="320">
                <VImg height="200px" :src="service.getChunkImageUrl(doc.chunkId)" cover></VImg>
                <VCardText class="pb-0">
                  <div class="d-flex align-center ga-2 mb-0">
                    <MimeIcon class="text-h1" :mime="doc.mime" />
                    <h2 class="text-truncate" :title="doc.name">{{ doc.name }}</h2>
                  </div>
                  <div class="text-body-2 text-medium-emphasis">
                    Загружено
                    <DateFmt :date="doc.createdAt" />
                  </div>
                </VCardText>
                <VCardActions>
                  <VBtn size="small" :href="service.getDocDownloadUrl(doc.docId)" target="_blank" :icon="mdiDownload" />
                  <VSpacer />
                  <VBtn size="small" @click="excludeChunk(doc.chunkId)">Исключить</VBtn>
                  <VBtn size="small" @click="interpretStore.interpret(doc.chunkId, lastSearchQuery)">Интерпретация</VBtn>
                  <VSpacer />
                  <VBtn size="small" @click="previewStore.preview(doc.docId, doc.pageId)" :icon="mdiEye" />
                </VCardActions>
              </VCard>
            </VCol>
          </VRow>
        </template>
      </VCol>
    </VRow>
  </VContainer>
</template>
