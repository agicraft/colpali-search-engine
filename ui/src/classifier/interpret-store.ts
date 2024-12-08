import { defineStore } from 'pinia';

export const useInterpretStore = defineStore('interpret', {
  state: () => ({
    chunkId: null as number | null,
    query: null as string | null,
  }),
  actions: {
    interpret(chunkId: number, query: string) {
      this.chunkId = chunkId;
      this.query = query;
    },
    hide() {
      this.chunkId = null;
      this.query = null;
    },
  },
});
