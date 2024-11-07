import { page } from '$app/stores';
import { onMount } from 'svelte';
import { extractNameAndIdFromPath, loadInfo } from '$lib/functions/player';
import { useData } from '$lib/functions/data';
import { goto } from '$app/navigation';
import { getUser } from '$lib/functions/user_check';
import { hostStore } from './stores/stores';

export {page, onMount, extractNameAndIdFromPath,
     loadInfo, useData, goto, getUser, hostStore}