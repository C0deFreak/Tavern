<script lang='ts'>
    import global_playlist from '$lib/stores/global_playlist';
    import Dropdown from '$lib/components/dropdown.svelte';
    import Player from "$lib/components/player.svelte";
    import type { AudioInfo } from "$lib/functions/player";
    import { afterNavigate } from '$app/navigation';
    import { hostStore, goto, useData, loadInfo } from '$lib/libraries'
    import { onMount } from 'svelte';
    import "../app.css";


    let position = 0;
    let play = '';  // Holds the current audio source URL
    let isPlaying = false;  // Indicates whether audio is playing or paused
    let play_text = 'Play';  // Button text
    let current_playlist: AudioInfo[] = [];
    let random = false;
    let current_audio: AudioInfo;

    interface GetNotifications {
        context: string[];
        link: string[];
        date: string[];
    }

    let notificationInfo: GetNotifications;

    function shuffle() {
        current_playlist.sort((a, b) => parseFloat(a.id.toString()) - parseFloat(b.id.toString()));

        if (random) {
            let currentIndex = current_playlist.length;

            while (currentIndex != 0) {

                let randomIndex = Math.floor(Math.random() * currentIndex);
                currentIndex--;

                [current_playlist[currentIndex], current_playlist[randomIndex]] = [
                current_playlist[randomIndex], current_playlist[currentIndex]];
            }
        }

        position = 0;
        isPlaying = false;
        play_text = 'Play';
        playPlaylist()
    }
  
    // Play the next song in the playlist
    function playPlaylist() {
        if (position < current_playlist.length) {
            current_audio = current_playlist[position]
            play = $hostStore + "/audio/file/" + current_audio.id.toString();

            position++;
        }
        if (position == current_playlist.length) {
            position = 0;
        };
        
    }
  
    // Toggle play/pause state
    function changePlayState() {
        isPlaying = !isPlaying;
        play_text = isPlaying ? 'Pause' : 'Play';
    }

     $: if (current_playlist.sort() !== $global_playlist && $global_playlist) {
        current_playlist = $global_playlist;
        position = 0;
        isPlaying = true;
        play_text = 'Pause';
        playPlaylist();
    }
        
    async function logout() {
        const response = await useData('/auth/logout', 'GET')

        if (response.ok) {
            goto('/auth/login')
        } else {
            goto('/');
        }
    }

    function skipSong(next: boolean) {
        console.log(!next);
        if (!next) {
            if (position <= 1) {
                position = current_playlist.length - (2 - position);
            } else {
                position = position - 2;
            }
            
        }
        playPlaylist();
    }

    // Load notifications initially
    async function loadNotifications() {
        notificationInfo = await loadInfo('', '_ignorename', '/auth/notifications');
    }

    // Reload notifications on page navigation (or change)
    afterNavigate(() => {
        loadNotifications(); // Reload notifications after page update
    });

    onMount(async () => {
        await loadNotifications();
        getPlaylists(); // Initial load on component mount
    });


    // Search
    interface GetItem {
        id: number;
        name: string;
        item_type: string;
    }

    let search = '';
    let quickList: GetItem[] = [];
    let savedPlaylists: GetItem[] = [];
    let searchedInfo = { link: [], context: [] }; // Example structure for notifications

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
        const response = await useData('/playlist/saved', 'GET');

        if (response.ok) {
            const data = await response.json();
            savedPlaylists = data.playlists as GetItem[];
        } else {
            savedPlaylists = [];
        }
    }

</script>

// Bottom
<nav class="fixed bottom-0 w-full bg-black text-white flex flex-col items-center justify-center p-4">
    {#if current_audio}
        <h3 class="text-lg font-bold">{current_audio.name}</h3>
        <h4 class="text-sm text-gray-400">{current_audio.author}</h4>

        <!-- Player component -->
        <Player {play} {isPlaying} on:audioEnded={playPlaylist} />

        <!-- Controls -->
        <div class="flex items-center gap-4 mt-2">
            <button on:click={changePlayState} class="px-4 py-2 bg-green-500 rounded">{play_text}</button>
            <input type="checkbox" bind:checked={random} on:change={shuffle} class="w-5 h-5">
            <button on:click={() => skipSong(false)} class="px-3 py-2 bg-neutral-900 rounded">&lt;&lt;</button>
            <button on:click={() => skipSong(true)} class="px-3 py-2 bg-neutral-900 rounded">&gt;&gt;</button>
        </div>
    {/if}
</nav>

// Top
<nav class="top-0 fixed bg-black w-full">
    <div class="flex justify-center items-center text-center">
        <div class="pr-4"><a class="bg-neutral-900 py-3 px-6 border border-neutral-300 rounded" href="/">Home</a></div>

        <input type="text" placeholder="Search..." bind:value={search} on:input={quickSerach}>
        
        <!-- Dropdown for Quick Search Results -->
        <Dropdown style={"nothing"} isOpen={quickList.length > 0}>
            {#if quickList.length > 0}
                {#each quickList as quick_info}
                    <div>
                        <a href={`/${quick_info.name.replace(/\s+/g, '-')}_${quick_info.item_type}id_${quick_info.id}`}>
                            {quick_info.name}
                        </a>            
                    </div>
                {/each}
            {/if}
        </Dropdown>
        
        <div class="px-4 fixed ml-[70%]">
            <Dropdown buttontext={"Notifications"} style={"bg-neutral-900 py-3 px-6 border border-neutral-300"}>
                {#if notificationInfo}
                    {#each notificationInfo.link as link, index}
                        <br>
                        <a href={link}>{notificationInfo.context[index]}</a>
                    {/each}
                {/if}
            </Dropdown>
        </div>

        <div class="px-4">
            <button class="bg-neutral-900 py-3 px-6 border border-neutral-300" on:click={logout}>Log Out</button>
        </div>
    </div>
</nav>

<nav class="fixed left-0 top-0 bg-black h-full flex flex-col items-start pt-[2%] px-3">
    <a class="bg-neutral-900 py-3 px-3 border border-neutral-300 text-xs mb-4" href="/upload">Upload</a>
    <a class="bg-neutral-900 py-3 px-3 border border-neutral-300 text-xs" href="/make-playlist">Playlist</a>

    {#if savedPlaylists.length > 0}
        {#each savedPlaylists as saved}
            <div>
                <a href={`/${saved.name.replace(/\s+/g, '-')}_playlistid_${saved.id}`}>
                    <button> {saved.name}</button>
                </a>         
            </div>
        {/each}
    {/if}
</nav>


<body class="bg-neutral-900 text-white font-mono font-semibold">
    <slot></slot>
</body>
