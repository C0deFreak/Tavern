<script lang="ts">
    import type { AudioInfo } from '$lib/functions/player';
    import Modal from '$lib/components/modal.svelte';
    import global_playlist from '$lib/stores/global_playlist';
    import { page, onMount, extractNameAndIdFromPath,
        useData, goto, getUser, loadInfo
     } from '$lib/libraries'

    $: ({ name, id } = extractNameAndIdFromPath($page.url.pathname, "audioid"));

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
    let user_id: number;
    let remove = false;

    onMount(async() => {
        user_id = await getUser();
        audioInfo = await loadInfo(id, name, '/audio/info/');
        getPlaylists();
    });

    function playPlaylist() {
        global_playlist.set([audioInfo]);
        $global_playlist = $global_playlist;
        isBeingPlayed = 'Currently Playing';
    }


    async function getPlaylists() {
        const response = await useData('/audio/used_in/' + id, 'GET');

        if (response.ok) {
            const data = await response.json();
            
            savedPlaylists = data.used_playlists as GetItem[];
        } else {
            savedPlaylists = [];
        }
    }

    async function editPlaylistContent(playlist_id: number) {
        const response = await useData('/playlist/edit_content/' + playlist_id + '/' + id, 'POST');
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

            await useData('/audio/edit/' + id, 'POST', formData);
            
            edited = false;
            goto($page.url.pathname)
            
        }
    }

    if (edited && !show) {
        goto($page.url.pathname)
    }

    async function deleteAudio() {
        if (!remove) {
            remove = !remove
        } else {
            const response = await useData('/audio/delete/' + id, 'POST');
            if (response.ok) {
                goto('/')
            }
        }
    }

</script>

{#if audioInfo}
    <h1>{audioInfo.name}</h1>
    <h4>{audioInfo.genre}</h4>
    <h3>Made by: {audioInfo.author}</h3>
    <h5>Listens: {audioInfo.listens}</h5>
    <p>About: {audioInfo.description}</p>
    <button on:click={playPlaylist}>{isBeingPlayed}</button>
    {#if user_id}
        <Modal >
            <a href="/make-playlist">New playlist</a>
            <h1>Playlists:</h1>
            {#each savedPlaylists as playlist}
                <h2>{playlist.name}</h2>
                <input type="checkbox" bind:checked={playlist.used} on:change={() => editPlaylistContent(playlist.id)}>
                <br>
            {/each}
        </Modal>
    {/if}
    {#if user_id == audioInfo.user_id}
        <Modal {text} bind:show={show} >
            <input type="text" bind:value={audioInfo.name} on:input={() => edited = true} placeholder="Name">
            <br>
            <input type="text" bind:value={audioInfo.description} on:input={() => edited = true} placeholder="Description">
            <br>
            <input type="text" bind:value={audioInfo.genre} on:input={() => edited = true} placeholder="Genre">
            <br>
            <input type="text" bind:value={audioInfo.author} on:input={() => edited = true} placeholder="Author">
            <input type="checkbox" bind:checked={audioInfo.is_private} on:change={() => edited = true}>
            <button on:click={deleteAudio}>Delete (needs 2 clicks)</button>
            {#if edited}
                <button on:click={editPlaylist}>Submit</button>
            {/if}
        </Modal>
    {/if}
{/if}

