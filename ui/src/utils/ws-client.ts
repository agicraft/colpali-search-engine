export interface WsClientOpts {
  uri: string;
  requestHandler: (data: any) => Promise<any>;
  statusChangeListener: () => void;
}

export type Disconnector = () => void;

export class WsClient {
  private socket: WebSocket | undefined;
  private stopped = false;

  constructor(private opts: WsClientOpts) {}

  private notifyStatusChanged() {
    if (this.opts.statusChangeListener) {
      this.opts.statusChangeListener();
    }
  }

  public isConnected() {
    return this.socket !== undefined;
  }

  public stop() {
    this.stopped = true;
    if (this.socket) {
      this.socket.close();
      this.socket = undefined;
    }
  }

  public start() {
    const RECONNECT_MS = 3000;

    const connect = () => {
      // check if it is reconnection and already stopped in between of waiting
      if (this.stopped) {
        return;
      }

      if (this.socket) {
        console.error('WS: Already connected');
        return;
      }

      console.log('WS: Connecting...');
      this.socket = new WebSocket(this.opts.uri);

      this.socket.onopen = () => {
        console.log('WS: Connected');
        this.notifyStatusChanged();
      };

      this.socket.onmessage = async (ev) => {
        const requestData = ev.data;
        console.log('WS: Received: ', requestData);
        const handlerResp = await this.opts.requestHandler(JSON.parse(requestData));
        if (handlerResp === undefined) {
          console.log('WS: Response not requested');
          return;
        }
        const responseData = JSON.stringify(handlerResp);
        // check if connection is still active
        if (this.socket) {
          console.log('WS: Sending: ', responseData);
          this.socket.send(responseData);
        } else {
          console.warn('WS: Failed to answer, socked closed');
        }
      };

      this.socket.onclose = () => {
        console.log('WS: Closed');
        this.socket = undefined;
        this.notifyStatusChanged();
        if (this.stopped) {
          return;
        }
        console.log(`WS: Reconnection in ${RECONNECT_MS}ms`);
        setTimeout(connect, RECONNECT_MS);
      };
    };
    connect();
  }
}
