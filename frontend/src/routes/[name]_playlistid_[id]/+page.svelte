<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import { extractNameAndIdFromPath, loadInfo } from '$lib/functions/player';
    import global_playlist from '$lib/stores/global_playlist';
    import type { AudioInfo } from '$lib/functions/player';
    import { useData } from '$lib/functions/data';
    import { goto } from '$app/navigation';
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
    const show = false;
    const text = '...';
    


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

    async function editPlaylist(audio_id: number) {
        const response = await useData('/edit_playlist_' + id + '/' + audio_id, 'POST');
        if (response.ok) {
            goto($page.url.pathname)
        }
    }
 

</script>

{#if playlistInfo}
    <h1>{playlistInfo.name}</h1>
    <h3>Made by: {playlistInfo.author}</h3>

    <p>About: {playlistInfo.description}</p>

    <br>
    <button on:click={playPlaylist}>{isBeingPlayed}</button>
    <Modal {show} {text} >
        <input type="text" value={playlistInfo.name} placeholder="Name">
        <input type="text" value={playlistInfo.description} placeholder="Description">
        <input type="text" value={playlistInfo.author} placeholder="Author">
    </Modal>

    <h2>Includes:</h2>
    {#if audioInfos.length > 0}
        {#each audioInfos as audioInfo}
            <div>
                <a href={`/${audioInfo.name.replace(/\s+/g, '-')}_id_${audioInfo.id}`}>
                    <h3> - {audioInfo.name}</h3>
                    <button on:click={() => editPlaylist(audioInfo.id)}>-</button>
                </a>         
            </div>
        {/each}
    {/if}
{/if}
