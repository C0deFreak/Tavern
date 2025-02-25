import { writable } from 'svelte/store';
import type { AudioInfo } from '$lib/functions/player';

const global_playlist: AudioInfo[] = [];
export default writable(global_playlist);
