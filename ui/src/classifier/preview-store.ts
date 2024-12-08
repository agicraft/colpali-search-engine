import { defineStore } from 'pinia';

export const usePreviewStore = defineStore('preview', {
  state: () => ({
    docId: null as number | null,
    pageId: null as number | null,
  }),
  actions: {
    preview(docId: number, pageId?: number) {
      this.docId = docId;
      this.pageId = pageId || null;
    },
    hide() {
      this.docId = null;
      this.pageId = null;
    },
  },
});
