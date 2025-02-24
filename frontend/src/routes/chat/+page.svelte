<script lang="ts">
    import type { AudioInfo } from '$lib/functions/player';
    import Dropdown from '$lib/components/dropdown.svelte';
    import global_playlist from '$lib/stores/global_playlist';
    import { page, onMount, extractNameAndIdFromPath,
        useData, goto, getUser, loadInfo
     } from '$lib/libraries'


    let code = '';

    onMount(async() => {
        await getUser(true);
    });

    async function redirectToRoom() {
        goto('/chat/' + code)
    }

    
</script>


<input class=" bg-neutral-600 rounded-1 py-2 px-2" type="text" placeholder="Chat Code" bind:value={code}>