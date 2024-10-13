<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { extractNameAndIdFromPath, loadInfo } from '$lib/functions/player';
    import global_playlist from '$lib/stores/global_playlist';
    import type { AudioInfo } from '$lib/functions/player';
    import Modal from '$lib/components/modal.svelte';

    $: ({ name, id } = extractNameAndIdFromPath($page.url.pathname, "playlistid"));

    interface PlaylistInfo {
        id: number;
        name: string;
        author: string;
        description: string;
        audio_ids: number[];
    }

    let playlistInfo: PlaylistInfo;
    let audioInfos: AudioInfo[] = [];
    let isBeingPlayed = 'Play'
    let show = false;


    async function loadAllAudioInfo(audio_ids: number[]) {
        audioInfos = await Promise.all(audio_ids.map(id => loadInfo(id.toString(), '_playlist', '/info/')));
        audioInfos.sort((a, b) => parseFloat(a.id.toString()) - parseFloat(b.id.toString()));
    }

    onMount(async() => {
        playlistInfo = await loadInfo(id, name, '/playlist/');
        await loadAllAudioInfo(playlistInfo.audio_ids);
            if ($global_playlist == audioInfos) {
                isBeingPlayed = 'Currently Playing'
            };
    });

    function playPlaylist() {
        global_playlist.set(audioInfos);
        $global_playlist = $global_playlist;
        isBeingPlayed = 'Currently Playing';
    }

    

</script>

{#if playlistInfo}
    <h1>{playlistInfo.name}</h1>
    <h3>Made by: {playlistInfo.author}</h3>

    <p>About: {playlistInfo.description}</p>

    <br>
    <button on:click={playPlaylist}>{isBeingPlayed}</button>
    <button on:click={() => show = !show}>+</button>
    <Modal {show} >
        <h1>Playlists:</h1>
    </Modal>

    <h2>Includes:</h2>
    {#if audioInfos.length > 0}
        {#each audioInfos as audioInfo}
            <div>
                <a href={`/${audioInfo.name.replace(/\s+/g, '-')}_id_${audioInfo.id}`}>
                    <h3> - {audioInfo.name}</h3>
                </a>         
            </div>
        {/each}
    {/if}
{/if}
