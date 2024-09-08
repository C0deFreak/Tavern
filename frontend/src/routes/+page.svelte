<title>Play</title>
<script lang="ts">
    import { hostStore } from '$lib/stores.js';
    import { goto } from '$app/navigation';


    interface AudioItem {
        id: number;
        name: string;
    }

    let search = '';
    let audioList: AudioItem[] = [];

    async function serachAudio() {
        const formData = new FormData();
        formData.append('search', search)

        const response = await fetch($hostStore + '/index', {
            method: 'POST',
            body: formData,
            credentials: 'include',
        });

        if (response.ok) {
            const data = await response.json();
            audioList = data.audio_files as AudioItem[]; // Populate the list of audio files
        } else {
            const data = await response.json();
            alert(data.error || "Search failed");
        }
    }

    async function logout() {
        const response = await fetch($hostStore + '/auth/logout', {
            method: 'GET',
            credentials: 'include'
        });

        const data = await response.json();
        if (response.ok) {
            alert('Logged out successfully');
            goto('auth/login')
        } else {
            alert('Logout failed: ' + data.error);
        }
    }
</script>


<input type="text" placeholder="Search..." bind:value={search}>
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
