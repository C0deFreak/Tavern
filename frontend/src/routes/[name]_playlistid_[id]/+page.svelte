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
        is_private: boolean;
    }

    let playlistInfo: PlaylistInfo;
    let audioInfos: AudioInfo[] = [];
    let isBeingPlayed = 'Play'
    let show = false;
    const text = '...';
    let edited = false;
    


    async function loadAllAudioInfo(audio_ids: number[]) {
        audioInfos = await Promise.all(audio_ids.map(id => loadInfo(id.toString(), '_playlist', '/audio/info/')));
        audioInfos.sort((a, b) => parseFloat(a.id.toString()) - parseFloat(b.id.toString()));
    }

    onMount(async() => {
        playlistInfo = await loadInfo(id, name, '/playlist/info/');
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

    async function editPlaylistContent(audio_id: number) {
        const response = await useData('/playlist/edit_content/' + id + '/' + audio_id, 'POST');
        if (response.ok) {
            goto($page.url.pathname)
        }
    }

    async function editPlaylist() {
        if (edited) {
            const formData = new FormData();
            formData.append('name', playlistInfo.name);
            formData.append('description', playlistInfo.description);
            formData.append('is_private', playlistInfo.is_private.toString());

            await useData('/playlist/edit/' + id, 'POST', formData);
            
            edited = false;
            goto($page.url.pathname)
            
        }
    }

    if (edited && !show) {
        goto($page.url.pathname)
    }
 

</script>

{#if playlistInfo}
    <h1>{playlistInfo.name}</h1>
    <h3>Made by: {playlistInfo.author}</h3>

    <p>About: {playlistInfo.description}</p>

    <br>
    <button on:click={playPlaylist}>{isBeingPlayed}</button>
    <Modal {text} bind:show={show} >
        <input type="text" bind:value={playlistInfo.name} on:input={() => edited = true} placeholder="Name">
        <br>
        <input type="text" bind:value={playlistInfo.description} on:input={() => edited = true} placeholder="Description">
        <br>
        <input type="checkbox" bind:checked={playlistInfo.is_private} on:change={() => edited = true}>
        {#if edited}
            <button on:click={editPlaylist}>Submit</button>
        {/if}
    </Modal>

    <h2>Includes:</h2>
    {#if audioInfos.length > 0}
        {#each audioInfos as audioInfo}
            <div>
                <a href={`/${audioInfo.name.replace(/\s+/g, '-')}_audioid_${audioInfo.id}`}>
                    <h3> - {audioInfo.name}</h3>
                    <button on:click={() => editPlaylistContent(audioInfo.id)}>-</button>
                </a>         
            </div>
        {/each}
    {/if}
{/if}
