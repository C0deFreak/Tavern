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

    let specialChars =/[`%^_*()\+=\[\]{};\\|<>\/?~]/

  
    onMount(async () => {
        getUser(true);
    });
  
    async function makePlaylist() {
            if (name.length > 100 || name.length < 1) {
                goto('/make-playlist');
            } else if (description.length > 500) {
                goto('/make-playlist');
            } else if (specialChars.test(name)) {
                goto('/make-playlist');
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

    async function quickSerach() {
        if (search.length > 0) {
            const formData = new FormData();
            formData.append('search', search)
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

    function addAudio(added_id: number) {
        if (!added_audio.includes(added_id)) {
            added_audio = [...added_audio, added_id];
        } else {
            added_audio = added_audio.filter(id => id !== added_id);
        }
    }

</script>

<div class="w-full h-1/2 fixed top-0 left-0 -z-10 mt-16 ml-49 rounded-2xl px-6 py-16" style="background: linear-gradient(to bottom, darkolivegreen, #171717);">
    <!-- File input and upload button -->
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="text" placeholder="Name" bind:value={name}>
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="text" placeholder="Description (optional)" bind:value={description}>
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="text" placeholder="Search..." bind:value={search} on:input={quickSerach}>

    {#if quickList.length > 0}
        {#each quickList as quick_info}
            <div class=" bg-neutral-900">
                <h6>{quick_info.name}</h6>
                <button class="px-4 py-2 bg-green-500 rounded-2xl text-xs" on:click={() => addAudio(quick_info.id)}>{added_audio.includes(quick_info.id) ? "-" : "+"}</button>         
            </div>
        {/each}
    {/if}
    <br>
    <p>Upload privately?</p>
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="checkbox" bind:checked={private_playlist}>
    <br>
    <button class="px-4 py-2 bg-green-500 rounded-2xl text-xs" on:click={makePlaylist}>Make playlist</button>

</div>
  