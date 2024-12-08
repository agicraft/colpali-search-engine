import { onBeforeMount, onUnmounted, ref } from 'vue';
import { WsClient } from './ws-client';

export const useWs = <T>(uri: string) => {
  const ret = ref<T>();

  const wsClient = new WsClient({
    uri,
    async requestHandler(data) {
      ret.value = data;
    },
    statusChangeListener() {
      console.log('WS Status: ' + wsClient.isConnected());
    },
  });

  onBeforeMount(() => {
    wsClient.start();
  });
  onUnmounted(() => {
    wsClient.stop();
  });
  return ret;
};
