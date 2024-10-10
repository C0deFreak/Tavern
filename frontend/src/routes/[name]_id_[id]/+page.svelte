<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import global_playlist from '$lib/stores/global_playlist';
    import { extractNameAndIdFromPath, loadInfo } from '$lib/functions/player';
    import type { AudioInfo } from '$lib/functions/player';

    $: ({ name, id } = extractNameAndIdFromPath($page.url.pathname, "id"));

    let audioInfo: AudioInfo;
    let isBeingPlayed = 'Play'
    

    onMount(async() => {
        audioInfo = await loadInfo(id, name, '/info/');
    });

    function playPlaylist() {
        global_playlist.set([Number(id)]);
        $global_playlist = $global_playlist;
        isBeingPlayed = 'Currently Playing';
    }

</script>

{#if audioInfo}
    <h1>{audioInfo.name}</h1>
    <h4>{audioInfo.genre}</h4>
    <h3>Made by: {audioInfo.author}</h3>

    <p>About: {audioInfo.description}</p>
    <button on:click={playPlaylist}>{isBeingPlayed}</button>
{/if}

