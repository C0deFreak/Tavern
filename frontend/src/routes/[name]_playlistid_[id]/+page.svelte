<script lang="ts">
    import global_playlist from '$lib/stores/global_playlist';
    import type { AudioInfo } from '$lib/functions/player';
    import Modal from '$lib/components/modal.svelte';
    import { page, onMount, extractNameAndIdFromPath,
        useData, goto, getUser, loadInfo
     } from '$lib/libraries'


    $: ({ name, id } = extractNameAndIdFromPath($page.url.pathname, "playlistid"));

    interface PlaylistInfo {
        id: number;
        name: string;
        author: string;
        description: string;
        audio_ids: number[];
        is_private: boolean;
        user_id: number;
    }

    let playlistInfo: PlaylistInfo;
    let audioInfos: AudioInfo[] = [];
    let isBeingPlayed = 'Play'
    let show = false;
    const text = '...';
    let edited = false;
    let remove = false;
    let user_id: number;
    
    


    async function loadAllAudioInfo(audio_ids: number[]) {
        audioInfos = await Promise.all(audio_ids.map(id => loadInfo(id.toString(), '_playlist', '/audio/info/')));
        audioInfos.sort((a, b) => parseFloat(a.id.toString()) - parseFloat(b.id.toString()));
    }

    onMount(async() => {
        user_id = await getUser();
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

    async function deletePlaylist() {
        if (!remove) {
            remove = !remove
        } else {
            const response = await useData('/playlist/delete/' + id, 'POST');
            if (response.ok) {
                goto('/')
            }
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
    {#if user_id == playlistInfo.user_id}
        <Modal {text} bind:show={show} >
            <input type="text" bind:value={playlistInfo.name} on:input={() => edited = true} placeholder="Name">
            <br>
            <input type="text" bind:value={playlistInfo.description} on:input={() => edited = true} placeholder="Description">
            <br>
            <input type="checkbox" bind:checked={playlistInfo.is_private} on:change={() => edited = true}>
            <button on:click={deletePlaylist}>Delete (needs 2 clicks)</button>
            {#if edited}
                <button on:click={editPlaylist}>Submit</button>
            {/if}
        </Modal>
    {/if}
    

    <h2>Includes:</h2>
    {#if audioInfos.length > 0}
        {#each audioInfos as audioInfo}
            <div>
                <a href={`/${audioInfo.name.replace(/\s+/g, '-')}_audioid_${audioInfo.id}`}>
                    <h3> - {audioInfo.name}</h3>
                    {#if user_id == playlistInfo.user_id}
                        <button on:click={() => editPlaylistContent(audioInfo.id)}>-</button>
                    {/if}
                </a>         
            </div>
        {/each}
    {/if}
{/if}
