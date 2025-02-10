<script lang="ts">
    import Dropdown from '$lib/components/dropdown.svelte';
    import global_playlist from '$lib/stores/global_playlist';
    import type { AudioInfo } from '$lib/functions/player';
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
    let edited = false;
    let remove = false;
    let user_id: number;
    let randomColor = '';
    
    


    async function loadAllAudioInfo(audio_ids: number[]) {
        audioInfos = await Promise.all(audio_ids.map(id => loadInfo(id.toString(), '_ignorename', '/audio/info/')));
        audioInfos.sort((a, b) => parseFloat(a.id.toString()) - parseFloat(b.id.toString()));
    }

    onMount(async() => {
        user_id = await getUser();
        playlistInfo = await loadInfo(id, name, '/playlist/info/');
        await loadAllAudioInfo(playlistInfo.audio_ids);
            if ($global_playlist == audioInfos) {
                isBeingPlayed = 'Currently Playing'
            };

        const allowedColors = [
        "red", "orange", "gold", "green",
        "teal", "blue", "indigo", "purple", "pink"
        ];

        // Pick a random color
        randomColor = allowedColors[Math.floor(Math.random() * allowedColors.length)];
        console.log(randomColor)
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
    <div class="w-full h-1/2 fixed top-0 left-0 -z-10 mt-16 ml-49 rounded-2xl px-6 py-16" style="background: linear-gradient(to bottom, {randomColor}, #171717);">
        <div class=" text-8xl font-extrabold">{playlistInfo.name}</div>
        <div class=" text-1xl font-semibold">{playlistInfo.author}</div>
        <div class=" text-xs font-normal"> ⦁ {playlistInfo.description}</div>

        <br>
        <button class=" px-4 py-2 bg-green-500 rounded-2xl text-xs" on:click={playPlaylist}>{isBeingPlayed}</button>
        {#if user_id == playlistInfo.user_id}
            <Dropdown style={"px-4 py-2 bg-neutral-700 text-xs rounded"}>
                <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="text" bind:value={playlistInfo.name} on:input={() => edited = true} placeholder="Name">
                <br>
                <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="text" bind:value={playlistInfo.description} on:input={() => edited = true} placeholder="Description">
                <br>
                <p>Is private <input type="checkbox" bind:checked={playlistInfo.is_private} on:change={() => edited = true}></p>
                <button class="px-4 py-2 bg-red-500 text-xs rounded" on:click={deletePlaylist}>Delete (needs 2 clicks)</button>
                {#if edited}
                    <button class="px-4 py-2 bg-green-500 rounded-2xl text-xs" on:click={editPlaylist}>Submit</button>
                {/if}
            </Dropdown>
        {/if}
        
        <br>
        <br>
        <h2 class=" text-2xl">Includes:</h2>
        {#if audioInfos.length > 0}
            {#each audioInfos as audioInfo}
                <div>
                    <a href={`/${audioInfo.name.replace(/\s+/g, '-')}_audioid_${audioInfo.id}`}>
                        <button class=" bg-neutral-700 py-1 px-2 border border-neutral-300 text-s mb-2">{audioInfo.name}</button> 
                    </a>   
                    {#if user_id == playlistInfo.user_id} 
                        <button class="px-2 py-1 bg-red-500 text-xs rounded" on:click={() => editPlaylistContent(audioInfo.id)}>-</button> 
                    {/if}      
                </div>
            {/each}
        {/if}
    </div>
{/if}
