<script lang="ts">
    import type { AudioInfo } from '$lib/functions/player';
    import Dropdown from '$lib/components/dropdown.svelte';
    import global_playlist from '$lib/stores/global_playlist';
    import { page, onMount, extractNameAndIdFromPath,
        useData, goto, getUser, loadInfo
     } from '$lib/libraries'

    // Izvlačenje imena i ID-a iz URL-a
    $: ({ name, id } = extractNameAndIdFromPath($page.url.pathname, "audioid"));

    interface GetItem {
        id: number;
        name: string;
        used: boolean;
    }

    let audioInfo: AudioInfo;
    let isBeingPlayed = 'Play'
    let show = false;
    let savedPlaylists: GetItem[] = [];
    let edited = false;
    let user_id: number;
    let remove = false;
    let report_info = '';
    let randomColor = '';

    // Montiranje komponente i dohvaćanje podataka o audio datoteci
    onMount(async() => {
        audioInfo = await loadInfo(id, name, '/audio/info/');
        user_id = await getUser();
        if (user_id != audioInfo.user_id) {
            user_id = await getUser(false, true);
        }
        getPlaylists();

        const allowedColors = [
        "red", "orange", "gold", "green",
        "teal", "blue", "indigo", "purple", "pink"
        ];

        // Odabir nasumične boje
        randomColor = allowedColors[Math.floor(Math.random() * allowedColors.length)];
    });

    // Funkcija za pokretanje audio zapisa u globalnu playlistu
    function playPlaylist() {
        global_playlist.set([audioInfo]);
        $global_playlist = $global_playlist;
        isBeingPlayed = 'Currently Playing';
    }

    // Dohvaćanje playlista u kojima je audio zapis
    async function getPlaylists() {
        const response = await useData('/audio/used_in/' + id, 'GET');

        if (response.ok) {
            const data = await response.json();
            
            savedPlaylists = data.used_playlists as GetItem[];
        } else {
            savedPlaylists = [];
        }
    }

    // Funkcija za uređivanje sadržaja playliste
    async function editPlaylistContent(playlist_id: number) {
        const response = await useData('/playlist/edit_content/' + playlist_id + '/' + id, 'POST');
        if (response.ok) {
            getPlaylists();
        }
    }

    // Funkcija za uređivanje audio zapisa
    async function editPlaylist() {
        if (edited) {
            const formData = new FormData();
            formData.append('name', audioInfo.name);
            formData.append('description', audioInfo.description);
            formData.append('author', audioInfo.author);
            formData.append('genre', audioInfo.genre);
            formData.append('is_private', audioInfo.is_private.toString());

            await useData('/audio/edit/' + id, 'POST', formData);
            
            edited = false;
            goto($page.url.pathname)
        }
    }

    // Funkcija za brisanje audio zapisa
    async function deleteAudio() {
        if (!remove) {
            remove = !remove;
        } else {
            const response = await useData('/audio/delete/' + id, 'POST');
            if (response.ok) {
                goto('/');
            }
        }
    }

    // Funkcija za prijavu audio zapisa
    async function reportAudio() {
        const formData = new FormData();
        formData.append('context', report_info);
        formData.append('name', audioInfo.name);

        await useData('/audio/report/' + id, 'POST', formData);
        
        location.reload();
    }

</script>

{#if audioInfo}
    <div class="w-full h-1/2 fixed top-0 left-0 -z-10 mt-16 ml-49 rounded-2xl px-6 py-16" style="background: linear-gradient(to bottom, {randomColor}, #171717);">
        <!-- Naziv audio zapisa -->
        <div class="text-8xl font-extrabold truncate w-400">{audioInfo.name}</div>

        <!-- Detalji o audio zapisu -->
        <div class="text-1xl font-normal">
            <a class="text-1xl font-semibold" href="{audioInfo.author.replace(/\s+/g, '-')}_userid_{audioInfo.user_id}">{audioInfo.author}</a> ⦁ {audioInfo.genre} ⦁ {audioInfo.listens} listens
        </div>
        <div class="text-xs font-normal"> ⦁ {audioInfo.description}</div>
        <br>
        
        <!-- Gumb za pokretanje audio zapisa -->
        <button class="px-4 py-2 bg-green-500 rounded-2xl text-xs" on:click={playPlaylist}>{isBeingPlayed}</button>
        
        {#if user_id == audioInfo.user_id}
            <!-- Dropdown za uređivanje audio zapisa -->
            <Dropdown style={"px-4 py-2 bg-neutral-700 text-xs rounded"}>
                <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="text" bind:value={audioInfo.name} on:input={() => edited = true} maxlength=100 placeholder="Name">
                <br>
                <textarea class="bg-neutral-900 rounded py-2 px-2 mt-2" bind:value={audioInfo.description} on:input={() => edited = true} placeholder="Description" maxlength=300 cols=21 rows=4></textarea>
                <br>
                <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="text" bind:value={audioInfo.genre} on:input={() => edited = true} maxlength=30 placeholder="Genre">
                <br>
                <p>Is private <input type="checkbox" bind:checked={audioInfo.is_private} on:change={() => edited = true}></p>
                <button class="px-4 py-2 bg-red-500 text-xs rounded" on:click={deleteAudio}>Delete (needs 2 clicks)</button>
                {#if edited}
                    <button class="px-4 py-2 bg-green-500 rounded text-xs" on:click={editPlaylist}>Submit</button>
                {/if}
            </Dropdown>
        {/if}

        {#if user_id}
            <!-- Dropdown za dodavanje u playlistu -->
            <Dropdown buttontext={"Add to playlist"} style={"px-4 py-2 bg-neutral-700 text-xs rounded"}>
                <a href="/make-playlist"><button class="px-4 py-2 bg-green-500 rounded-2xl text-xs">New playlist</button></a>
                <h1>Playlists:</h1>
                {#each savedPlaylists as playlist}
                    <h2 class=" truncate">{playlist.name}</h2>
                    <input type="checkbox" bind:checked={playlist.used} on:change={() => editPlaylistContent(playlist.id)}>
                    <br>
                {/each}
            </Dropdown>

            <!-- Dropdown za prijavu audio zapisa -->
            <Dropdown buttontext={"Report audio"} style={"px-4 py-2 bg-red-500 text-xs rounded"}>
                <h3>Reason for report:</h3>
                <textarea class="bg-neutral-900 rounded py-2 px-2 mt-2" placeholder="I reported this..." maxlength=255 cols=21 rows=4 bind:value={report_info}></textarea>
                <button class="px-4 py-2 bg-red-500 text-xs rounded" on:click={reportAudio}>Submit</button>
            </Dropdown>
        {/if}

        {#if user_id == -1}
            <!-- Gumb za brisanje od strane admina -->
            <button class="px-4 py-2 bg-red-500 text-xs rounded" on:click={deleteAudio}>Admin delete (needs 2 clicks)</button>
        {/if}
    </div>
{/if}
