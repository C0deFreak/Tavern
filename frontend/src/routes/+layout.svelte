<script lang='ts'>
    import global_playlist from '$lib/stores/global_playlist';
    import Player from "$lib/components/player.svelte";
    import type { AudioInfo } from "$lib/functions/player";
    import { hostStore, goto, useData } from '$lib/libraries'
    
    let position = 0;
    let play = '';  // Holds the current audio source URL
    let isPlaying = false;  // Indicates whether audio is playing or paused
    let play_text = 'Play';  // Button text
    let current_playlist: AudioInfo[] = [];
    let random = false;
    let current_audio: AudioInfo;

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
            location.reload()
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

  </script>
  
  <nav>
    {#if current_audio}
        <h3>{current_audio.name}</h3>
        <h4>{current_audio.author}</h4>
        <br>
    {/if}
    <!-- Player component, no play/pause button, controlled by the layout -->
    <Player {play} {isPlaying} on:audioEnded={playPlaylist} />
  
    <!-- Play/Pause button to control playback -->
    <button on:click={changePlayState}>{play_text}</button>
    <input type="checkbox" bind:checked={random} on:change={shuffle}>
    <button on:click={() => skipSong(false)}>&lt;&lt;</button>
    <button on:click={() => skipSong(true)}>&gt;&gt;</button>
    <br>
    <a href="/">Home</a>
    <a href="/upload">Upload</a>
    <a href="/make-playlist">New Playlist</a>
    <button on:click={logout}>Log Out</button>
  </nav>
  
  <slot></slot>
  