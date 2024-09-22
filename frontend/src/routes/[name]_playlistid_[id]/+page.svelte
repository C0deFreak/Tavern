<script lang="ts">
    import { page } from '$app/stores';
    import { hostStore } from '$lib/stores';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { useData } from '$lib/data';

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
    let position = 0;
    let play = "";
    let random = false;
    let playlist: number[];


    export async function loadInfo() {    
        const response = await useData('/playlist/' + id, 'GET')

        if (response.ok) {
            playlistInfo = await response.json();
            if (name !== playlistInfo.name.replace(/\s+/g, '-')) {
                goto('/');
            }
            // Load audio information for all audio_ids
            await loadAllAudioInfo(playlistInfo.audio_ids);
            playlist = playlistInfo.audio_ids;
            playPlaylist();
        } else {
            goto('/');
        }
    }

    export async function loadAudioInfo(get_id: number) {    
        const response = await useData('/info/' + get_id.toString(), 'GET');
        if (response.ok) {
            return await response.json();
        }
        return null;
    }

    async function loadAllAudioInfo(audio_ids: number[]) {
        audioInfos = await Promise.all(audio_ids.map(id => loadAudioInfo(id)));
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

    function playPlaylist() {     
        play = $hostStore + "/audio/" + playlist[position].toString();
        const player = (document.getElementById("player") as HTMLAudioElement | null);
        if (player) {
            player.load();

            if (position != 0) {
                player.play();
            } else {
                player.pause();
            }
        }

        if (position < playlist.length - 1) {
            position++;
        } else {
            position = 0;
        }
       
    }

    function shuffle() {
        playlist = playlistInfo.audio_ids;

        if (random) {
            let currentIndex = playlist.length;

            while (currentIndex != 0) {

                let randomIndex = Math.floor(Math.random() * currentIndex);
                currentIndex--;

                [playlist[currentIndex], playlist[randomIndex]] = [
                playlist[randomIndex], playlist[currentIndex]];
            }
        }

        play = $hostStore + "/audio/" + playlist[0].toString();
        const player = (document.getElementById("player") as HTMLAudioElement | null);
        if (player) {
            player.load();
        }
    }

    onMount(() => {
        loadInfo();
    });

</script>

{#if playlistInfo}
    <h1>{playlistInfo.name}</h1>
    <h3>Made by: {playlistInfo.author}</h3>

    <p>About: {playlistInfo.description}</p>

    <p>Shuffle</p>
    <input type="checkbox" bind:checked={random} on:change={shuffle}>
    <br>

    <!-- Audio Player -->
    <audio on:ended={playPlaylist} id="player" controls>
        <source src={play}>
    </audio>

    <br>

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
