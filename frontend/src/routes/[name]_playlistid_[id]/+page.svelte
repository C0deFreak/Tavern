<script lang="ts">
    import Dropdown from '$lib/components/dropdown.svelte';
    import global_playlist from '$lib/stores/global_playlist';
    import type { AudioInfo } from '$lib/functions/player';
    import { page, onMount, extractNameAndIdFromPath,
        useData, goto, getUser, loadInfo
     } from '$lib/libraries'


    // Izvlačenje imena i ID-a iz URL-a za playlistu
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
    
    // Funkcija za učitavanje svih informacija o audiosnimkama unutar playliste
    async function loadAllAudioInfo(audio_ids: number[]) {
        audioInfos = await Promise.all(audio_ids.map(id => loadInfo(id.toString(), '_ignorename', '/audio/info/')));
        audioInfos.sort((a, b) => parseFloat(a.id.toString()) - parseFloat(b.id.toString()));
    }

    // Montiranje komponente i dohvaćanje podataka o playlisti
    onMount(async() => {
        user_id = await getUser();
        playlistInfo = await loadInfo(id, name, '/playlist/info/');
        await loadAllAudioInfo(playlistInfo.audio_ids);
            if ($global_playlist == audioInfos) {
                isBeingPlayed = 'Currently Playing'
            };

        // Popis dopuštenih boja za pozadinu
        const allowedColors = [
        "red", "orange", "gold", "green",
        "teal", "blue", "indigo", "purple", "pink"
        ];

        // Odabir nasumične boje
        randomColor = allowedColors[Math.floor(Math.random() * allowedColors.length)];
    });

    // Funkcija za pokretanje playliste
    function playPlaylist() {
        global_playlist.set(audioInfos);
        $global_playlist = $global_playlist;
        isBeingPlayed = 'Currently Playing';
    }

    // Funkcija za uređivanje sadržaja playliste
    async function editPlaylistContent(audio_id: number) {
        const response = await useData('/playlist/edit_content/' + id + '/' + audio_id, 'POST');
        if (response.ok) {
            location.reload()
        }
    }

    // Funkcija za uređivanje same playliste
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

    // Funkcija za brisanje playliste
    async function deletePlaylist() {
        if (!remove) {
            remove = !remove;
        } else {
            const response = await useData('/playlist/delete/' + id, 'POST');
            if (response.ok) {
                goto('/')
            }
        }
    }

    // Preusmjeravanje korisnika nakon što je playlistu uređena
    if (edited && !show) {
        goto($page.url.pathname)
    }
</script>

{#if playlistInfo}
    <div class="w-full h-1/2 fixed top-0 left-0 -z-10 mt-16 ml-49 rounded-2xl px-6 py-16" style="background: linear-gradient(to bottom, {randomColor}, #171717);">
        <!-- Ime playliste -->
        <div class="text-8xl font-extrabold truncate w-400">{playlistInfo.name}</div>

        <!-- Autor playliste -->
        <div class="text-1xl font-semibold">{playlistInfo.author}</div>

        <!-- Opis playliste -->
        <div class="text-xs font-normal"> ⦁ {playlistInfo.description}</div>

        <br>

        <!-- Gumb za pokretanje playliste -->
        <button class="px-4 py-2 bg-green-500 rounded-2xl text-xs" on:click={playPlaylist}>{isBeingPlayed}</button>

        {#if user_id == playlistInfo.user_id}
            <!-- Dropdown za uređivanje playliste -->
            <Dropdown style={"px-4 py-2 bg-neutral-700 text-xs rounded"}>
                <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="text" bind:value={playlistInfo.name} on:input={() => edited = true} maxlength=100 placeholder="Name">
                <br>
                <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="text" bind:value={playlistInfo.description} on:input={() => edited = true} maxlength=300 placeholder="Description">
                <br>
                <button class="px-4 py-2 bg-red-500 text-xs rounded" on:click={deletePlaylist}>Delete (needs 2 clicks)</button>
                {#if edited}
                    <button class="px-4 py-2 bg-green-500 rounded-2xl text-xs" on:click={editPlaylist}>Submit</button>
                {/if}
            </Dropdown>
        {/if}
        
        <br>
        <br>
        <!-- Popis audio zapisa u playlisti -->
        <h2 class="text-2xl mb-4">Includes:</h2>
        <div class="grid grid-cols-3 gap-2 max-h-60 overflow-y-auto w-150">
            {#if audioInfos.length > 0}
                {#each audioInfos as audioInfo}
                    <div class="relative w-40 h-15 border border-neutral-300 bg-neutral-700 flex items-center justify-center rounded">
                        <!-- Cijeli pravokutnik je klikabilan -->
                        <a href={`/${audioInfo.name.replace(/\s+/g, '-')}_audioid_${audioInfo.id}`} class="absolute inset-0 z-0 flex items-center justify-center text-center">
                            <div class="z-10 text-white text-center px-1 truncate">{audioInfo.name}</div>
                        </a>
                        
                        {#if user_id == playlistInfo.user_id}
                            <!-- Tipka za brisanje; zaustavlja prosljeđivanje klika -->
                            <button class="absolute top-1 right-1 px-2 py-1 bg-red-500 text-xs rounded z-20" on:click={() => editPlaylistContent(audioInfo.id)}>
                                -
                            </button>
                        {/if}
                    </div>
                {/each}
            {/if}
        </div>
        

    </div>
{/if}
