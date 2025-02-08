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
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }

    /* Main container for controls */
    .controls-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        width: 600px; /* Adjust width as needed */
    }

    /* Time display (left & right of progress bar) */
    .time {
        font-size: 14px;
        color: #555;
        min-width: 40px; /* Ensures consistent width */
        text-align: center;
    }

    /* Progress bar container */
    .progress-container {
        display: flex;
        align-items: center;
        flex: 1;
        margin: 0 10px; /* Spacing between time & bar */
    }

    /* Progress bar (seek bar) */
    .progress-bar {
        -webkit-appearance: none;
        appearance: none;
        width: 100%;
        height: 6px;
        background: #ddd;
        border-radius: 5px;
        outline: none;
    }

    /* WebKit (Chrome, Safari) - Track */
    .progress-bar::-webkit-slider-runnable-track {
        width: 100%;
        height: 6px;
        border-radius: 5px;
        background: linear-gradient(to right, #1ed760 var(--progress, 0%), #ddd var(--progress, 0%)); 
    }

    /* WebKit - Thumb */
    .progress-bar::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: #1ed760;
        cursor: pointer;
        margin-top: -4px; /* Align thumb properly */
        position: relative;
    }

    /* Firefox - Track */
    .progress-bar::-moz-range-track {
        width: 100%;
        height: 6px;
        border-radius: 5px;
        background: #ddd;
    }

    /* Firefox - Progress */
    .progress-bar::-moz-range-progress {
        background: #1ed760;
        height: 6px;
        border-radius: 5px;
    }

    /* Volume control on the far right */
    .volume-control {
        width: 100px;
        height: 6px;
        margin-left: 20px; /* Separates from total time */
        -webkit-appearance: none;
        appearance: none;
        background: #ddd;
        border-radius: 5px;
    }

    /* Volume control - Thumb */
    .volume-control::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #1ed760;
        cursor: pointer;
    }

    /* Volume control - Firefox */
    .volume-control::-moz-range-thumb {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #1ed760;
        cursor: pointer;
    }

</style>
  
<div class="audio-player">  
    <audio id="audio">
        <source src={play}>
        Your browser does not support the audio element.
    </audio>

    <!-- Controls structured like Spotify -->
    <div class="controls-container">
        <div id="current-time" class="time">0:00</div>

        <div class="progress-container">
            <input type="range" id="progress-bar" class="progress-bar" min="0" max="0" step="1" value="0">
        </div>

        <div id="total-time" class="time">0:00</div>

        <input type="range" id="volume-control" class="volume-control" min="0" max="1" step="0.01" value="1">
    </div>
</div>  
