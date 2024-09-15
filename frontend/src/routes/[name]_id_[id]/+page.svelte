<script lang="ts">
    import { page } from '$app/stores';
    import { hostStore } from '$lib/stores';
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
    import { useData } from '$lib/data';

    $: ({ name, id } = extractNameAndIdFromPath($page.url.pathname));

    interface AudioInfo {
        id: number;
        name: string;
        author: string;
        genre: string;
        description: string;

    }
    let audioInfo: AudioInfo;
    


    export async function loadInfo() {    
        const response = await useData('/info/' + id, 'GET')

        if (response.ok) {
            audioInfo = await response.json();
            if (name != audioInfo.name.replace(/\s+/g, '-')) {
                goto('/');
            }
        } else {
            goto('/');
        }
        
    }

    function extractNameAndIdFromPath(path: string) {
        // Adjust the regex to capture the name and ID from the URL
        const match = path.match(/(.+)_id_(\d+)$/);
        if (match) {
            return {
                name: match[1].slice(1),  // Extracted name
                id: match[2]     // Extracted ID
            };
        }
        return { name: 'Not Found', id: 'Not Found' };
    }

    onMount(() => {
        loadInfo();
    });

    

</script>

{#if audioInfo}
    <h1>{audioInfo.name}</h1>
    <h4>{audioInfo.genre}</h4>
    <h3>Made by: {audioInfo.author}</h3>

    <p>About: {audioInfo.description}</p>
    <audio controls>
        <source src="{$hostStore}/audio/{id}">
    </audio>
{/if}

