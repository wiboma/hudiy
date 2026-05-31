export class HudiyClient {
  constructor(url) {
    this.url = url;
    this.socket = null;
    this.onMessage = null;
    this.onOpen = null;
    this.onClose = null;
  }

  connect() {
    return new Promise((resolve, reject) => {
      this.socket = new WebSocket(this.url);
      this.socket.binaryType = "arraybuffer";

      this.socket.onopen = () => {
        if (this.onOpen) this.onOpen();
        resolve();
      };

      this.socket.onmessage = (event) => {
        const msg = this._parseMessage(event.data);
        if (this.onMessage) this.onMessage(msg);
      };

      this.socket.onerror = reject;
      this.socket.onclose = () => {
        if (this.onClose) this.onClose();
      };
    });
  }

  sendMessage(id, flags, payload) {
    const header = new ArrayBuffer(12);
    const view = new DataView(header);
    view.setUint32(0, payload.length, true);
    view.setUint32(4, id, true);
    view.setUint32(8, flags, true);

    const full = new Uint8Array(12 + payload.length);
    full.set(new Uint8Array(header), 0);
    full.set(payload, 12);
    this.socket.send(full);
  }

  _parseMessage(buffer) {
    const view = new DataView(buffer);
    const len = view.getUint32(0, true);
    const id = view.getUint32(4, true);
    const flags = view.getUint32(8, true);
    const payload = new Uint8Array(buffer.slice(12));
    return { id, flags, payload };
  }

  disconnect() {
    if (this.socket && this.socket.readyState === WebSocket.OPEN)
      this.socket.close();
  }
}