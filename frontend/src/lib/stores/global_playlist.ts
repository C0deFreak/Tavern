import { writable } from 'svelte/store'; // Uvoz writable funkcije iz Svelte store
import type { AudioInfo } from '$lib/functions/player'; // Tip za AudioInfo

// Inicijalizacija prazne globalne liste pjesama
const global_playlist: AudioInfo[] = [];

// Kreiranje writable store-a za globalnu playlistu
export default writable(global_playlist);
