<script lang='ts'>
    import { hostStore } from "$lib/stores";
    import global_playlist from "$lib/global_playlist";
    import Player from "$lib/components/player.svelte";
    
    let position = 0;
    let play = '';  // Holds the current audio source URL
    let isPlaying = false;  // Indicates whether audio is playing or paused
    let play_text = 'Play';  // Button text
    let current_playlist: number[] = [];
    let random = false;

    function shuffle() {
        current_playlist.sort();

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
            play = $hostStore + "/audio/" + current_playlist[position].toString();
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

     $: if (current_playlist.sort() !== $global_playlist && $global_playlist[0]) {
        current_playlist = $global_playlist;
        console.log(current_playlist);
        position = 0;
        isPlaying = true;
        play_text = 'Pause';
        playPlaylist();
    }
        
    console.log(isPlaying);
  </script>
  
  <nav>
    <!-- Player component, no play/pause button, controlled by the layout -->
    <Player {play} {isPlaying} on:audioEnded={playPlaylist} />
  
    <!-- Play/Pause button to control playback -->
    <button on:click={changePlayState}>{play_text}</button>
    <input type="checkbox" bind:checked={random} on:change={shuffle}>
    <a href="/">Home</a>
    <a href="/upload">Upload</a>
    <a href="/make-playlist">New Playlist</a>
  </nav>
  
  <slot></slot>
  