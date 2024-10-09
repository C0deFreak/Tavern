<script lang="ts">
    import { page } from '$app/stores';
    import { hostStore } from '$lib/stores';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { useData } from '$lib/data';
    import global_playlist from '$lib/global_playlist';

    $: ({ name, id } = extractNameAndIdFromPath($page.url.pathname));

    interface PlaylistInfo {
        id: number;
        name: string;
        author: string;
        description: string;
        audio_ids: number[];
    }

    interface AudioInfo {
        id: number;
        name: string;
        author: string;
        genre: string;
    }

    let playlistInfo: PlaylistInfo;
    let audioInfos: AudioInfo[] = [];
    let isBeingPlayed = 'Play'


    export async function loadInfo() {    
        const response = await useData('/playlist/' + id, 'GET')

        if (response.ok) {
            playlistInfo = await response.json();
            if (name !== playlistInfo.name.replace(/\s+/g, '-')) {
                goto('/');
            }
            // Load audio information for all audio_ids
            await loadAllAudioInfo(playlistInfo.audio_ids);
            if ($global_playlist == playlistInfo.audio_ids) {
                isBeingPlayed = 'Currently Playing'
            };
        } else {
            goto('/');
        }
    }

    export async function loadSingleAudioInfo(get_id: number) {    
        const response = await useData('/info/' + get_id.toString(), 'GET');
        if (response.ok) {
            return await response.json();
        }
        return null;
    }

    async function loadAllAudioInfo(audio_ids: number[]) {
        audioInfos = await Promise.all(audio_ids.map(id => loadSingleAudioInfo(id)));
    }

    function extractNameAndIdFromPath(path: string) {
        const match = path.match(/(.+)_playlistid_(\d+)$/);
        if (match) {
            return {
                name: match[1].slice(1),
                id: match[2]
            };
        }
        return { name: 'Not Found', id: 'Not Found' };
    }

    onMount(() => {
        loadInfo();
    });

    function playPlaylist() {
        global_playlist.set(playlistInfo.audio_ids);
        $global_playlist = $global_playlist;
        isBeingPlayed = 'Currently Playing';
    }

    

</script>

{#if playlistInfo}
    <h1>{playlistInfo.name}</h1>
    <h3>Made by: {playlistInfo.author}</h3>

    <p>About: {playlistInfo.description}</p>

    <p>Shuffle</p>

    <br>
    <button on:click={playPlaylist}>{isBeingPlayed}</button>

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
