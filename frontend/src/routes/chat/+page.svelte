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

    async function makeRoom() {
        const response = await useData('/chat/create', 'POST');
        if (response.ok) {
            const code = await response.json();
            goto('/chat/' + code.code)
        }
    }

</script>


<input class=" bg-neutral-600 rounded-1 py-2 px-2" type="text" placeholder="Chat Code" bind:value={code}>
<button class="px-4 py-2 bg-red-500 text-xs rounded" on:click={redirectToRoom}>Submit</button>

<button class="px-4 py-2 bg-green-500 text-xs rounded" on:click={makeRoom}>Make room</button>