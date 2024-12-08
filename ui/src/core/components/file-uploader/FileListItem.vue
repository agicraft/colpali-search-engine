<script setup lang="ts">
import {
  onMounted,
  ref,
} from 'vue';
import { getSizeWithUnit } from './shared.helper';
import type { FileUploadInterface } from './shared.interface';
import { upload } from '@/utils/http';
import { VListItem, VListItemTitle, VProgressLinear } from 'vuetify/components';
import { mdiCheckCircleOutline, mdiProgressClose, mdiProgressUpload } from '@mdi/js';

interface PropsInterface {
  item: FileUploadInterface;
  uploadUrl: string;
}

const props = defineProps<PropsInterface>();

const progress = ref(0);

const isUploaded = ref(false);
const isFailed = ref(false)
const errorMessage = ref('')

function onUploadProgress({ loaded, total }: ProgressEvent): void {
  progress.value = loaded / total;
}

onMounted(async () => {
  const formData = new FormData();

  formData.append('file', props.item.file);

  try {
    await upload({
      method: 'POST',
      url: props.uploadUrl,
      onProgress: onUploadProgress,
      formData,
    })
    isUploaded.value = true;
  } catch (e) {
    isFailed.value = true
    errorMessage.value = String(e)
  }
});

</script>

<template>
  <VListItem>
    <template v-slot:prepend>
      <VIcon v-if="isFailed" :icon="mdiProgressClose" color="error" size="large" />
      <VIcon v-else-if="isUploaded" :icon="mdiCheckCircleOutline" color="success" size="large" />
      <VIcon v-else :icon="mdiProgressUpload" color="info" size="large"></VIcon>
    </template>

    <VListItemTitle>{{ props.item.file.name }}</VListItemTitle>
    <div v-if="isFailed" class="text-error">{{ errorMessage }}</div>
    <div v-else-if="isUploaded" class="text-success">
      {{ getSizeWithUnit(props.item.file.size) }}
    </div>
    <template v-else>
      <VProgressLinear v-model="progress" color="primary" height="25">
        <template v-slot:default="{ value }">
          <span>
            {{ getSizeWithUnit(props.item.file.size * value) }} / {{ getSizeWithUnit(props.item.file.size) }}
            ({{ Math.ceil(value) }}%)
          </span>
        </template>
      </VProgressLinear>
    </template>
  </VListItem>
</template>
