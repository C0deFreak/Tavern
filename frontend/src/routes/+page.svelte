<title>Play</title>
<script lang="ts">
    import { goto } from '$app/navigation';
    import { useData } from '$lib/functions/data';
    import { onMount } from 'svelte';


    interface GetItem {
        id: number;
        name: string;
    }

    let search = '';
    let quickList: GetItem[] = [];
    let savedPlaylists: GetItem[] = [];


    async function quickSerach() {
        if (search.length > 0) {
            const formData = new FormData();
            formData.append('search', search)
            formData.append('showPrivate', "true")
            const response = await useData('/search', 'POST', formData)


            if (response.ok) {
                const data = await response.json();
                quickList = data.audio_files as GetItem[];
            }    
        } else {
            quickList = [];
        }  
    }

    async function getPlaylists() {
        const response = await useData('/saved', 'GET');

        if (response.ok) {
            const data = await response.json();
            savedPlaylists = data.playlists as GetItem[];
        } else {
            savedPlaylists = [];
        }
    }

    onMount (() => {
        getPlaylists();
    });

</script>


<input type="text" placeholder="Search..." bind:value={search} on:input={quickSerach}>

{#if quickList.length > 0}
    {#each quickList as quick_info}
        <div>
            <a href={`/${quick_info.name.replace(/\s+/g, '-')}_id_${quick_info.id}`}>
                {quick_info.name}
            </a>            
        </div>
    {/each}
{/if}
<br>

<br>
{#if savedPlaylists.length > 0}
    {#each savedPlaylists as saved}
        <div>
            <a href={`/${saved.name.replace(/\s+/g, '-')}_playlistid_${saved.id}`}>
                <button> {saved.name}</button>
            </a>         
        </div>
    {/each}
{/if}
