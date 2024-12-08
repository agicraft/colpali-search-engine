<script setup lang="ts">
import { mdiUpload } from '@mdi/js';
import { ref } from 'vue';

interface PropsInterface {
  label: string;
}

const props = defineProps<PropsInterface>();

const emit = defineEmits<{
  (e: 'file-input-change', uploadFiles: File[]): void,
}>();

const formRef = ref<HTMLFormElement>();

const inputRef = ref<HTMLInputElement>();

function onFormClick(): void {
  inputRef.value?.click();
}

function onFormDrop(event: DragEvent): void {
  const files = Array.from(event.dataTransfer?.files || []);

  if (!files.length) return;

  emit('file-input-change', files);
  formRef.value?.classList.remove('active');
}

function onFormDragOver(): void {
  formRef.value?.classList.add('active');
}

function onFormDragLeave(): void {
  formRef.value?.classList.remove('active');
}

function onInputChange(): void {
  const files = Array.from(inputRef.value?.files || []);

  if (!files.length) return;

  emit('file-input-change', files);
  formRef.value?.reset();
}
</script>

<template>
  <form ref="formRef" :class="$style.form" class="d-flex pa-4 justify-center align-center flex-column cursor-pointer"
    @click="onFormClick()" @drop.prevent="onFormDrop($event)" @dragover.prevent="onFormDragOver()"
    @dragleave.prevent="onFormDragLeave()">
    <VIcon class="upload-icon" :icon="mdiUpload" :size="80"></VIcon>
    <div v-if="props.label" class="mb-4 text-center">
      {{ props.label }}
    </div>
    <input ref="inputRef" type="file" multiple class="d-none" @change="onInputChange()">
  </form>
</template>

<style module lang="scss">
.form {
  border: 1px dashed rgb(var(--v-theme-primary));
  border-radius: 10px;
  color: rgb(var(--v-theme-secondary));

  :global(.upload-icon) {
    transition: transform .25s ease;
  }

  &:global(.active),
  &:hover {
    color: rgb(var(--v-theme-primary));

    :global(.upload-icon) {
      transform: scale(1.25);
    }
  }
}
</style>
