import { io } from "socket.io-client";
import { hostStore } from './stores/stores';

let url;

hostStore.subscribe(value => {
  url = value;
  console.log(url)
})();

export const socket = io(url, { withCredentials: true });

socket.on("connect", () => {
  console.log("Socket connected:", socket.id);
});