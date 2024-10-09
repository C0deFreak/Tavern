<script lang="ts">
    import { onMount, createEventDispatcher } from "svelte";
  
    export let play: string; // The current audio source (song URL)
    export let isPlaying: boolean; // Whether the audio should be playing or not

    let dispatch = createEventDispatcher();
    let audio: HTMLAudioElement | null = null;
  
    onMount(() => {
        audio = document.getElementById("audio")! as HTMLAudioElement;
    
        // Set volume control once
        const volumeControl = document.getElementById("volume-control")! as HTMLInputElement;
        volumeControl.addEventListener("input", () => {
            if (audio) {
                audio.volume = Number(volumeControl.value);
            }
        });
    
        // Time update logic to track progress
        const timeControl = document.getElementById("progress-bar")! as HTMLInputElement;

        // Initialize max to 0 on mount to avoid glitches
        timeControl.max = String(audio!.duration);

        timeControl.addEventListener("input", () => {
            if (audio) {
                audio.currentTime = Number(timeControl.value);
            }
        });

        audio.addEventListener("loadedmetadata", () => {
            // Update max when the audio metadata is loaded
            if (audio) {
                timeControl.max = String(audio.duration);
                timeControl.value = String(audio.currentTime); // Set initial value
            }
        });

        audio.addEventListener("timeupdate", () => {
            const currentTimeDisplay = document.getElementById("current-time")!;
            const totalTimeDisplay = document.getElementById("total-time")!;
            
            if (audio) {
                timeControl.value = String(audio.currentTime); // Update value with current time
            }

            const currentMinutes = Math.floor(audio!.currentTime / 60);
            const currentSeconds = Math.floor(audio!.currentTime % 60);
            const totalMinutes = Math.floor(audio!.duration / 60);
            const totalSeconds = Math.floor(audio!.duration % 60);
    
            currentTimeDisplay.textContent = `${currentMinutes}:${currentSeconds < 10 ? '0' : ''}${currentSeconds}`;
            totalTimeDisplay.textContent = `${totalMinutes}:${totalSeconds < 10 ? '0' : ''}${totalSeconds}`;
        });

        audio.addEventListener("ended", () => {
            dispatch('audioEnded');
        });
    });

    // Reactively update the player when `play` or `isPlaying` changes
    $: if (audio && play) {
        if (audio.src !== play) {
            audio.src = play;  // Only set the source when it changes
            audio.load();
            
            if (isPlaying) {
                audio.play();
            }         
        } else {
            if (isPlaying) {
                audio.play();
            } else {
                audio.pause();
            }
        }
    }
</script>
  
<style>
    .audio-player {
        width: 400px;
        margin: 20px;
    }
  
    .controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 10px;
    }
  
    .progress {
        height: 10px;
        background-color: #ccc;
        margin-top: 10px;
    }

    /* General styling for the progress bar */
    .progress-bar {
        -webkit-appearance: none; /* Remove default styling */
        appearance: none; /* Remove default styling */
        width: 400px; /* Set explicit width to 400px */
        height: 6px; /* Height of the track */
        background: #ddd; /* Background color of the track */
        border-radius: 5px; /* Rounded corners */
        outline: none; /* Remove outline */
    }

    /* Styling the thumb for WebKit browsers */
    .progress-bar::-webkit-slider-thumb {
        -webkit-appearance: none; /* Remove default styling */
        appearance: none; /* Remove default styling */
        width: 20px; /* Width of the thumb */
        height: 20px; /* Height of the thumb */
        background: #1db954; /* Thumb color (Spotify green) */
        border: none; /* Remove border */
        border-radius: 50%; /* Rounded thumb */
        cursor: pointer; /* Change cursor on hover */
        box-shadow: 0 0 2px rgba(0, 0, 0, 0.5); /* Add shadow for depth */
        margin-top: -7px; /* Center thumb vertically on track */
    }

    /* Styling the thumb for Firefox */
    .progress-bar::-moz-range-thumb {
        width: 20px; /* Width of the thumb */
        height: 20px; /* Height of the thumb */
        background: #1db954; /* Thumb color (Spotify green) */
        border: none; /* Remove border */
        border-radius: 50%; /* Rounded thumb */
        cursor: pointer; /* Change cursor on hover */
    }

    /* Optional: Change track color on hover */
    .progress-bar:hover {
        background: #bbb; /* Darker track color on hover */
    }

    /* Optional: Change thumb color on hover */
    .progress-bar::-webkit-slider-thumb:hover {
        background: #1ed760; /* Lighter green on hover */
    }

    .progress-bar::-moz-range-thumb:hover {
        background: #1ed760; /* Lighter green on hover */
    }

    #current-time, #total-time {
        margin-top: 10px;
    }
</style>
  
<div class="audio-player">  
    <audio id="audio">
        <source src={play}>
        Your browser does not support the audio element.
    </audio>
    <div class="controls">
        <input type="range" id="volume-control" min="0" max="1" step="0.01" value="1">
    </div>
    <div class="progress">
        <input type="range" id="progress-bar" class="progress-bar" min="0" max="0" step="1" value="0">
    </div>
    <div id="current-time">0:00</div>
    <div id="total-time">0:00</div>
</div>  
