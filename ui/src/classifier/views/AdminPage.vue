<script setup lang="ts">
import FileUploader from '@/core/components/file-uploader/FileUploader.vue';
import { useService } from '@/utils/di';
import { VDialog } from 'vuetify/components';
import { ClassifierApiService } from '../ClassifierApiService';
import { reactive } from 'vue';
import { mdiCheckCircleOutline, mdiDelete, mdiDownload, mdiEye, mdiProgressWrench, mdiRefresh, mdiUpload } from '@mdi/js';
import {
  VToolbar,
  VDataTableServer,
  VSpacer,
  VTextField,
  VIcon,
  VBtn,
  VDivider,
} from 'vuetify/components'
import { ref } from 'vue';
import { FilteringQueryDt, mapDtToApiQuery } from '@/utils/helpers';
import type { DocumentDto } from '../classifier-dto';
import MimeIcon from '@/core/components/MimeIcon.vue';
import DateFmt from '@/core/components/DateFmt.vue';
import { usePageStore } from '@/core/page-store';
import AppHeader from '@/components/AppHeader.vue';
import PreviewPopup from '../components/PreviewPopup.vue';
import { usePreviewStore } from '../preview-store';

const service = useService(ClassifierApiService)

const pageStore = usePageStore();
const previewStore = usePreviewStore()

const serverItems = ref<DocumentDto[]>([])
const loading = ref(true)

const filteringQuery = reactive(new FilteringQueryDt())
filteringQuery.sortBy = [{ key: 'id', order: 'desc' }]
const totalItems = ref(0)


const loadItems = async () => {
  loading.value = true
  try {
    const { items, total } = await service.getDocuments(mapDtToApiQuery(filteringQuery));
    serverItems.value = items
    totalItems.value = total
  } catch (e) {
    pageStore.notifyException(e)
  }
  loading.value = false;
}

const deleteItem = async (item: DocumentDto) => {
  if (await pageStore.confirm("Отменить операцию будет невозможно. Удалить документ?")) {
    loading.value = true
    try {
      await service.deleteDocument(item.id);
      await loadItems()
    } catch (e) {
      pageStore.notifyException(e)
    }
    loading.value = false;
  }
}

const headers: any[] = [
  { key: 'id', title: '#', sortable: true, width: 30 },
  { key: 'mime', title: 'Тип', sortable: true, width: 30 },
  { key: 'createdAt', title: 'Дата загрузки', sortable: true, width: 60 },
  { key: 'name', title: 'Название документа', sortable: true },
  { key: 'numPages', title: 'Страниц (фрагментов)', sortable: false, width: 60 },
  { key: 'indexed', title: 'Статус', sortable: true, width: 60 },
  { key: 'actions', title: '', sortable: false, width: 140 },
]

</script>

<template>
  <PreviewPopup />
  <VContainer>
    <AppHeader class="mb-4" />

    <VDataTableServer v-model:items-per-page="filteringQuery.perPage" :headers="headers" :items="serverItems"
      v-model:page="filteringQuery.page" :items-per-page-options="[5, 10, 20, 50, 100]" :items-length="totalItems"
      :loading="loading" :search="filteringQuery.search" item-value="id" @update:options="loadItems"
      loading-text="Загрузка.." no-data-text="No data" v-model:sort-by="filteringQuery.sortBy">
      <template v-slot:item.createdAt="{ item }">
        <DateFmt :date="item.createdAt" />
      </template>
      <template v-slot:item.mime="{ item }">
        <MimeIcon :mime="item.mime" :size="32" />
      </template>
      <template v-slot:item.numPages="{ item }">
        {{ item.numPages }} ({{ item.numChunks }})
      </template>
      <template v-slot:item.name="{ item }">
        <div :class="$style.docName" :title="item.name">{{ item.name }}</div>
      </template>
      <template v-slot:item.indexed="{ item }">
        <VIcon v-if="item.indexed" color="success" :icon="mdiCheckCircleOutline" title="Проиндекирован" />
        <VIcon v-else color="info" :icon="mdiProgressWrench" title="Индексация" />
      </template>
      <template v-slot:item.actions="{ item }">
        <VBtn size="small" variant="flat" :icon="mdiEye" @click="previewStore.preview(item.id)" />
        <VBtn size="small" variant="flat" :href="service.getDocDownloadUrl(item.id)" target="_blank"
          :icon="mdiDownload" />
        <VBtn size="small" variant="flat" :icon="mdiDelete" @click="deleteItem(item)" />
      </template>
      <template v-slot:top>
        <VToolbar flat>
          <VTextField v-model="filteringQuery.search" class="ma-2" density="compact"
            placeholder="Быстрый поиск по названию" hide-details variant="outlined" />
          <VDivider class="mx-4" inset vertical />
          <VSpacer />
          <VBtn color="primary" @click="loadItems()" :prepend-icon="mdiRefresh">Обновить</VBtn>
          <VDialog max-width="500" @after-leave="loadItems">
            <template v-slot:activator="{ props: activatorProps }">
              <VBtn color="primary" v-bind="activatorProps" text="Загрузить документы" :prepend-icon="mdiUpload"></VBtn>
            </template>
            <template v-slot:default="{ isActive }">
              <VCard title="Загрузка документов">
                <VCardText class="pb-0">
                  <FileUploader :upload-url="service.getUploadEndpoint()"
                    label="Перетащите файлы сюда или кликните для выбора" />
                </VCardText>
                <VCardActions>
                  <VSpacer></VSpacer>
                  <VBtn text="Закрыть" @click="isActive.value = false"></VBtn>
                </VCardActions>
              </VCard>
            </template>
          </VDialog>
        </VToolbar>
      </template>
    </VDataTableServer>
  </VContainer>
</template>
<style module lang="scss">
.docName {
  word-break: break-all;
}
</style>
