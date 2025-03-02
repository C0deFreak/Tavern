<script lang="ts">
    import { onMount, goto, useData, getUser } from '$lib/libraries';

    let name = '';
    let description = '';
    let private_playlist = false;

    let added_audio: number[] = [];

    interface AudioItem {
        id: number;
        name: string;
    }

    let search = '';
    let quickList: AudioItem[] = [];

    let specialChars = /[`%^_*()\+=\[\]{};\\|<>\/?~]/

    // Dohvaćanje korisnika pri montaži komponente
    onMount(async () => {
        getUser(true);
    });
  
    // Funkcija za kreiranje playliste
    async function makePlaylist() {
        if (name.length > 100 || name.length < 1) {
            alert('Name too long or short');
        } else if (description.length > 500) {
            alert('Description too long');
        } else if (specialChars.test(name)) {
            alert('No special characters allowed in the name');
        } else {
            const formData = new FormData();
            formData.append('name', name);
            formData.append('description', description);
            formData.append('private', private_playlist.toString());
            formData.append('added_audio', JSON.stringify(added_audio));
            
            const response = await useData('/playlist/create', 'POST', formData);

            if (response.ok) {
                goto('/');
            }
        }
    }

    // Funkcija za brzo pretraživanje audio fajlova
    async function quickSerach() {
        if (search.length > 0) {
            const formData = new FormData();
            formData.append('search', search)
            formData.append('songs_only', 'true');
            formData.append('showPrivate', private_playlist.toString())
            const response = await useData('/search', 'POST', formData)

            if (response.ok) {
                const data = await response.json();
                quickList = data.audio_files as AudioItem[];
            }    
        } else {
            quickList = [];
        }
    }

    // Funkcija za dodavanje ili uklanjanje audiosnimke iz liste
    function addAudio(added_id: number) {
        if (!added_audio.includes(added_id)) {
            added_audio = [...added_audio, added_id];
        } else {
            added_audio = added_audio.filter(id => id !== added_id);
        }
    }
</script>

<div class="w-full h-1/2 fixed top-0 left-0 -z-10 mt-16 ml-49 rounded-2xl px-6 py-16" style="background: linear-gradient(to bottom, darkolivegreen, #171717);">
    <!-- Input za unos imena playliste -->
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="text" placeholder="Name" bind:value={name}>

    <!-- Input za unos opisa playliste -->
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="text" placeholder="Description (optional)" bind:value={description}>

    <!-- Input za pretragu audio fajlova -->
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="text" placeholder="Search..." bind:value={search} on:input={quickSerach}>

    {#if quickList.length > 0}
        <!-- Prikaz rezultata pretrage -->
        <div class="max-h-60 overflow-y-auto">
            {#each quickList as quick_info}
                <div class="bg-neutral-900 w-167">
                    <h6 class=" truncate">{quick_info.name}</h6>
                    <!-- Gumb za dodavanje ili uklanjanje audio fajla -->
                    <button class="px-4 py-2 bg-green-500 rounded-2xl text-xs" on:click={() => addAudio(quick_info.id)}>{added_audio.includes(quick_info.id) ? "-" : "+"}</button>         
                </div>
            {/each}
        </div>
    {/if}
    <br>
    
    <!-- Checkbox za odabir privatnosti playliste -->
    <p>Upload privately?</p>
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="checkbox" bind:checked={private_playlist}>
    <br>

    <!-- Gumb za kreiranje playliste -->
    <button class="px-4 py-2 bg-green-500 rounded-2xl text-xs" on:click={makePlaylist}>Make playlist</button>
</div>
