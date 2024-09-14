<title>Play</title>
<script lang="ts">
    import { hostStore } from '$lib/stores.js';
    import { goto } from '$app/navigation';


    interface AudioItem {
        id: number;
        name: string;
    }

    let search = '';
    let quick = '';
    let quickLenght = 2;
    let audioList: AudioItem[] = [];
    let quickList: AudioItem[] = [];

    async function serachAudio() {
        quick = '';
        const formData = new FormData();
        formData.append('search', search)
        formData.append('quick', quick)

        const response = await fetch($hostStore + '/index', {
            method: 'POST',
            body: formData,
            credentials: 'include',
        });

        if (response.ok) {
            const data = await response.json();
            audioList = data.audio_files as AudioItem[];
            console.log(audioList); // Populate the list of audio files
        } else {
            goto('/');
        }
    }

    async function quickSerach() {
        if (search.length >= quickLenght) {
            quick = '%'
            const formData = new FormData();
            formData.append('quick', quick)
            formData.append('search', search)
            const response = await fetch($hostStore + '/index', {
                method: 'POST',
                body: formData,
                credentials: 'include',
            });

            if (response.ok) {
                const data = await response.json();
                quickList = data.audio_files as AudioItem[];
            }
        } else {
            quick = ''
            quickList = [];
        }

        
    }

    async function logout() {
        const response = await fetch($hostStore + '/auth/logout', {
            method: 'GET',
            credentials: 'include'
        });

        if (response.ok) {
            goto('/auth/login')
        } else {
            goto('/');
        }
    }

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

<button on:click={serachAudio}>Search</button>

{#if audioList.length > 0}
    {#each audioList as audio}
        <div>
            <h3>{audio.name}</h3>
            <audio controls>
                <source src="{$hostStore}/audio/{audio.id}">
            </audio>
        </div>
    {/each}
{:else}
    <p>No audio found</p>
{/if}

<button on:click={logout}>Log Out</button>
