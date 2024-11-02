<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import global_playlist from '$lib/stores/global_playlist';
    import { extractNameAndIdFromPath, loadInfo } from '$lib/functions/player';
    import type { AudioInfo } from '$lib/functions/player';
    import Modal from '$lib/components/modal.svelte';
    import { useData } from '$lib/functions/data';
    import { goto } from '$app/navigation';

    $: ({ name, id } = extractNameAndIdFromPath($page.url.pathname, "id"));

    interface GetItem {
        id: number;
        name: string;
        used: boolean;
    }

    let audioInfo: AudioInfo;
    let isBeingPlayed = 'Play'
    const text = '...';
    let show = false;
    let savedPlaylists: GetItem[] = [];
    let edited = false;

    onMount(async() => {
        audioInfo = await loadInfo(id, name, '/info/');
        getPlaylists();
    });

    function playPlaylist() {
        global_playlist.set([audioInfo]);
        $global_playlist = $global_playlist;
        isBeingPlayed = 'Currently Playing';
    }


    async function getPlaylists() {
        const response = await useData('/get_in_playlists/' + id, 'GET');

        if (response.ok) {
            const data = await response.json();
            
            savedPlaylists = data.used_playlists as GetItem[];
        } else {
            savedPlaylists = [];
        }
    }

    async function editPlaylistContent(playlist_id: number) {
        const response = await useData('/edit_playlist_content_' + playlist_id + '/' + id, 'POST');
        if (response.ok) {
            getPlaylists()
        }
    }

    async function editPlaylist() {
        if (edited) {
            const formData = new FormData();
            formData.append('name', audioInfo.name);
            formData.append('description', audioInfo.description);
            formData.append('author', audioInfo.author);
            formData.append('genre', audioInfo.genre);
            formData.append('is_private', audioInfo.is_private.toString());

            await useData('/edit_audio_' + id, 'POST', formData);
            
            edited = false;
            goto($page.url.pathname)
            
        }
    }

    if (edited && !show) {
        goto($page.url.pathname)
    }

</script>

{#if audioInfo}
    <h1>{audioInfo.name}</h1>
    <h4>{audioInfo.genre}</h4>
    <h3>Made by: {audioInfo.author}</h3>

    <p>About: {audioInfo.description}</p>
    <button on:click={playPlaylist}>{isBeingPlayed}</button>
    <Modal >
        <a href="/make-playlist">New playlist</a>
        <h1>Playlists:</h1>
        {#each savedPlaylists as playlist}
            <h2>{playlist.name}</h2>
            <input type="checkbox" bind:checked={playlist.used} on:change={() => editPlaylistContent(playlist.id)}>
            <br>
        {/each}
    </Modal>
    <Modal {text} bind:show={show} >
        <input type="text" bind:value={audioInfo.name} on:input={() => edited = true} placeholder="Name">
        <br>
        <input type="text" bind:value={audioInfo.description} on:input={() => edited = true} placeholder="Description">
        <br>
        <input type="text" bind:value={audioInfo.genre} on:input={() => edited = true} placeholder="Genre">
        <br>
        <input type="text" bind:value={audioInfo.author} on:input={() => edited = true} placeholder="Author">
        <input type="checkbox" bind:checked={audioInfo.is_private} on:change={() => edited = true}>
        {#if edited}
            <button on:click={editPlaylist}>Submit</button>
        {/if}
    </Modal>
{/if}

