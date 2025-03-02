<script lang="ts">
    import global_playlist from '$lib/stores/global_playlist';
    import Dropdown from '$lib/components/dropdown.svelte';
    import Player from "$lib/components/player.svelte";
    import type { AudioInfo } from "$lib/functions/player";
    import { afterNavigate } from '$app/navigation';
    import { hostStore, goto, useData, loadInfo, getUser } from '$lib/libraries';
    import { onMount } from 'svelte';
    import "../app.css";
  
    let position = 0;
    let play = '';
    let isPlaying = false;
    let play_text = 'Play';
    let current_playlist: AudioInfo[] = [];
    let random = false;
    let current_audio: AudioInfo | null = null;
  
    interface GetItem {
      id: number;
      name: string;
      item_type: string;
    }
  
    let search = '';
    let quickList: GetItem[] = [];
    let savedPlaylists: GetItem[] = [];
  
    interface GetNotifications {
      context: string[];
      link: string[];
      date: string[];
    }
  
    let notificationInfo: GetNotifications;
    let user_id: number;
    let user_name: string;
  
    // Miješa trenutnu playlistu ako je opcija random uključena
    function shuffle() {
      current_playlist.sort((a, b) => parseFloat(a.id.toString()) - parseFloat(b.id.toString()));
      if (random) {
        let currentIndex = current_playlist.length;
        while (currentIndex !== 0) {
          let randomIndex = Math.floor(Math.random() * currentIndex);
          currentIndex--;
          [current_playlist[currentIndex], current_playlist[randomIndex]] = [current_playlist[randomIndex], current_playlist[currentIndex]];
        }
      }
      position = 0;
      isPlaying = false;
      play_text = 'Play';
      playPlaylist();
    }
  
    // Reprodukcija sljedeće pjesme u playlisti
    function playPlaylist() {
      if (position < current_playlist.length) {
        current_audio = current_playlist[position];
        play = $hostStore + "/audio/file/" + current_audio.id.toString();
        position++;
      }
      if (position === current_playlist.length) {
        position = 0;
      }
    }
  
    // Prekida ili nastavlja reprodukciju
    function changePlayState() {
      isPlaying = !isPlaying;
      play_text = isPlaying ? 'Pause' : 'Play';
    }
  
    // Ažurira trenutnu playlistu i postavlja reprodukciju
    $: if (current_playlist.sort() !== $global_playlist && $global_playlist) {
      current_playlist = $global_playlist;
      position = 0;
      isPlaying = true;
      play_text = 'Pause';
      playPlaylist();
    }
    $: if (!current_playlist.length) {
      isPlaying = false;
      current_audio = null;
    }
  
    // Odjava korisnika
    async function logout() {
      const response = await useData('/auth/logout', 'GET');
      if (response.ok) {
        goto('/auth/login');
      } else {
        goto('/');
      }
    }
  
    // Preskače pjesmu; next=true za iduću, false za prethodnu
    function skipSong(next: boolean) {
      if (!next) {
        if (position <= 1) {
          position = current_playlist.length - (2 - position);
        } else {
          position = position - 2;
        }
      }
      playPlaylist();
    }
  
    // Učitava obavijesti za korisnika
    async function loadNotifications() {
      notificationInfo = await loadInfo('', '_ignorename', '/auth/notifications');
    }
  
    // Nakon navigacije, osvježi obavijesti i pretraživanje te playliste
    afterNavigate(async () => {
      loadNotifications();
      search = '';
      quickSerach();
      getPlaylists();
      user_id = await getUser();
      if (user_id) {
        user_name = await getUser(true);
      };
    });
  
    // Inicijalno učitavanje obavijesti, playlista i korisnika
    onMount(async () => {
      await loadNotifications();
      getPlaylists();
      user_id = await getUser();
      if (user_id) {
        user_name = await getUser(true);
      };
    });
  
    // Brzo pretraživanje audio fajlova
    async function quickSerach() {
      if (search.length > 0) {
        const formData = new FormData();
        formData.append('search', search);
        formData.append('songs_only', 'false');
        formData.append('showPrivate', "true");
        const response = await useData('/search', 'POST', formData);
        if (response.ok) {
          const data = await response.json();
          quickList = data.audio_files as GetItem[];
        }
      } else {
        quickList = [];
      }
    }
  
    // Učitava spremljene playliste korisnika
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
  
  <!-- DONJA NAVIGACIJSKA TRAKA -->
  <nav class="fixed bottom-0 left-0 w-full bg-black text-white flex flex-col items-center justify-center p-4 z-20" data-sveltekit-keepfocus>
    {#if current_audio}
      <h3 class="text-lg font-bold">{current_audio.name}</h3>
      <h4 class="text-sm text-gray-400">{current_audio.author}</h4>
      <Player {play} {isPlaying} on:audioEnded={playPlaylist} />
      <div class="flex items-center gap-4 mt-2">
        <button on:click={changePlayState} class="px-4 py-2 bg-green-500 rounded">{play_text}</button>
        <input type="checkbox" bind:checked={random} on:change={shuffle} class="w-5 h-5">
        <button on:click={() => skipSong(false)} class="px-3 py-2 bg-neutral-900 rounded">&lt;&lt;</button>
        <button on:click={() => skipSong(true)} class="px-3 py-2 bg-neutral-900 rounded">&gt;&gt;</button>
      </div>
    {/if}
  </nav>
  
  <!-- GORNJA NAVIGACIJSKA TRAKA -->
  <nav class="top-0 fixed bg-black left-0 w-full h-15 py-1">
    <div class="flex justify-center items-center text-center">
      <div class="pr-4">
        <a class="bg-neutral-900 py-3 px-6 border border-neutral-300 rounded" href="/">Home</a>
      </div>
      <div class="relative">
        <input class="bg-neutral-900 rounded-3xl py-2 px-2" type="text" placeholder="Search..." bind:value={search} on:input={quickSerach}>
        {#if quickList.length > 0}
          <div class="absolute top-full left-0 bg-neutral-900 border border-gray-300 shadow-md z-[1000] max-h-[200px] overflow-y-auto w-full min-h-[50px] p-0 m-0 list-none">
            {#each quickList as quick_info}
              <div>
                <a href={`/${quick_info.name.replace(/\s+/g, '-')}_${quick_info.item_type}id_${quick_info.id}`}>
                  <button class="w-full py-2 hover:bg-neutral-800 bg-neutral-900 border border-gray-300 cursor-pointer truncate">{quick_info.name}</button>
                </a>
              </div>
            {/each}
          </div>
        {/if}
      </div>
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
            {#if user_id}
                <button class="bg-neutral-900 py-3 px-6 border border-neutral-300" on:click={logout}>Log Out</button>
                <button class="bg-neutral-900 py-3 px-6 border border-neutral-300" on:click={() => goto('/' + user_name + '_userid_' + user_id)}>{user_name}</button>
            {/if}   

            {#if !user_id}
                <button class="bg-neutral-900 py-3 px-6 border border-neutral-300" on:click={() => goto("/auth/login")}>Log In</button>
                <button class="bg-neutral-900 py-3 px-6 border border-neutral-300" on:click={() => goto("/auth/sign-up")}>Sign Up</button>
            {/if}
        </div>
  
    </div>
  </nav>
  
  <!-- LIJEVA NAVIGACIJSKA TRAKA -->
  <nav class="fixed left-0 top-0 bg-black h-screen w-48 p-3 z-10">
    <a class="block bg-neutral-900 py-3 px-3 border border-neutral-300 text-xs mb-4" href="/chat">Chat rooms</a>
    <a class="block bg-neutral-900 py-3 px-3 border border-neutral-300 text-xs mb-4" href="/upload">Upload</a>
    <a class="block bg-neutral-900 py-3 px-3 border border-neutral-300 text-xs mb-4" href="/make-playlist">Playlist</a>
    {#if savedPlaylists.length > 0}
      {#each savedPlaylists as saved}
        <a class="block bg-neutral-700 py-3 px-3 border border-neutral-300 text-xs mb-2 truncate" 
           href={`/${saved.name.replace(/\s+/g, '-')}_playlistid_${saved.id}`}>
          {saved.name}
        </a>
      {/each}
    {/if}
  </nav>
  
  <html lang="en" class="bg-neutral-900"></html>
  <body class="w-3/4 h-full text-white font-mono font-semibold p-4 mt-6 ml-25">
    <slot></slot>
  </body>
  