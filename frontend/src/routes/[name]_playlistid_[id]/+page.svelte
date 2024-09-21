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
    let playlistInfo: PlaylistInfo;
    let position = 0;
    let play = "";
    


    export async function loadInfo() {    
        const response = await useData('/playlist/' + id, 'GET')

        if (response.ok) {
            playlistInfo = await response.json();
            console.log(playlistInfo)
            if (name != playlistInfo.name.replace(/\s+/g, '-')) {
                goto('/');
            }
            playPlaylist();
        } else {
            goto('/');
        }
        
    }

    function extractNameAndIdFromPath(path: string) {
        // Adjust the regex to capture the name and ID from the URL
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
        play = $hostStore + "/audio/" + playlistInfo.audio_ids[position].toString()
        const player = (document.getElementById("player") as HTMLAudioElement | null);
        if (player) {
            player.load();
            if (position != 0) {
                player.play()
            } else {
                player.pause()
            }
        }

        if (position < playlistInfo.audio_ids.length - 1) {
            position++;
        } else {
            position = 0;
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
    <audio on:ended={playPlaylist} id="player" controls>
        <source src={play}>
    </audio>
{/if}

