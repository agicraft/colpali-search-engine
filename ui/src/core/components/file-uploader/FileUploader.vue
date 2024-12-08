<script setup lang="ts">
import { ref } from 'vue';
import { nanoid } from 'nanoid';
import FileInput from './FileInput.vue';
import { type FileUploadInterface } from './shared.interface';
import FileListItem from './FileListItem.vue';

const props = withDefaults(defineProps<{
  uploadUrl: string;
  label?: string;
}>(), {
  label: 'Browse files or drop them here',
});

const uploadFileList = ref<FileUploadInterface[]>([]);

async function onFileInputChange(uploadFiles: File[]): Promise<void> {
  uploadFileList.value = [
    ...uploadFiles.map((file) => ({
      id: nanoid(),
      file,
    })),
    ...uploadFileList.value,
  ];
}

</script>

<template>
  <section class="file-uploader">
    <FileInput :label="props.label" @file-input-change="onFileInputChange($event)" />
    <VList density="compact" v-if="uploadFileList.length" class="mt-4 overflow-y-visible" max-height="200">
      <FileListItem v-for="item in uploadFileList" :key="item.id" :item="item" :upload-url="props.uploadUrl" />
    </VList>
  </section>
</template>
