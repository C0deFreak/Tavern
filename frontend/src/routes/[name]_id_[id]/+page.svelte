<script lang="ts">
    import { page } from '$app/stores';
    import { onMount } from 'svelte';
    import global_playlist from '$lib/stores/global_playlist';
    import { extractNameAndIdFromPath, loadInfo } from '$lib/functions/player';
    import type { AudioInfo } from '$lib/functions/player';
    import Modal from '$lib/components/modal.svelte';
    import { useData } from '$lib/functions/data';

    $: ({ name, id } = extractNameAndIdFromPath($page.url.pathname, "id"));

    interface GetItem {
        id: number;
        name: string;
        used: boolean;
    }

    let audioInfo: AudioInfo;
    let isBeingPlayed = 'Play'
    let show = false;
    let savedPlaylists: GetItem[] = [];

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
            console.log(data);
            
            savedPlaylists = data.used_playlists as GetItem[];
        } else {
            savedPlaylists = [];
        }
    }

    async function editPlaylist(playlist_id: number) {
        const response = await useData('/edit_playlist_' + playlist_id + '/' + id, 'POST');
        if (response.ok) {
            getPlaylists()
        }
    }

</script>

{#if audioInfo}
    <h1>{audioInfo.name}</h1>
    <h4>{audioInfo.genre}</h4>
    <h3>Made by: {audioInfo.author}</h3>

    <p>About: {audioInfo.description}</p>
    <button on:click={playPlaylist}>{isBeingPlayed}</button>
    <Modal {show} >
        <h1>Playlists:</h1>
        {#each savedPlaylists as playlist}
            <h2>{playlist.name}</h2>
            <input type="checkbox" bind:checked={playlist.used} on:change={() => editPlaylist(playlist.id)}>
            <br>
        {/each}
    </Modal>
{/if}

