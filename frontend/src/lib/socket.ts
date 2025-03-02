import { io } from "socket.io-client"; // Uvoz Socket.io klijenta
import { hostStore } from './stores/stores'; // Uvoz store-a koji sadrži URL

let url;

// Pretplata na store za promjenu URL-a
hostStore.subscribe(value => {
  url = value; // Pohranjivanje vrijednosti URL-a
})();

// Inicijalizacija Socket.io klijenta s URL-om i podrškom za kolačiće
export const socket = io(url, { withCredentials: true });