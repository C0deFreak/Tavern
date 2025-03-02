<script lang="ts">
    import { onMount, createEventDispatcher } from "svelte";

    export let play: string; // Trenutni izvor zvuka (URL pjesme)
    export let isPlaying: boolean; // Ovisno o tome treba li zvuk biti u tijeku

    let dispatch = createEventDispatcher();
    let audio: HTMLAudioElement | null = null;
  
    // Sva logika koja se pokreće kada je komponenta učitana
    onMount(() => {
        audio = document.getElementById("audio")! as HTMLAudioElement;
    
        // Postavljanje kontrole glasnoće
        const volumeControl = document.getElementById("volume-control")! as HTMLInputElement;
        volumeControl.addEventListener("input", () => {
            if (audio) {
                audio.volume = Number(volumeControl.value); // Podešava glasnoću
            }
        });
    
        // Praćenje vremena i pomicanje progresije
        const timeControl = document.getElementById("progress-bar")! as HTMLInputElement;

        // Inicijaliziraj maksimalnu vrijednost kako bi izbjegao greške
        timeControl.max = String(audio!.duration);

        // Osvježava vrijeme kad korisnik pomiče progresiju
        timeControl.addEventListener("input", () => {
            if (audio) {
                audio.currentTime = Number(timeControl.value);
            }
        });

        // Kada su metapodaci audio datoteke učitani
        audio.addEventListener("loadedmetadata", () => {
            if (audio) {
                timeControl.max = String(audio.duration);
                timeControl.value = String(audio.currentTime); // Postavi početnu vrijednost
            }
        });

        // Ažuriranje vremena kad se zvuk reproducira
        audio.addEventListener("timeupdate", () => {
            const currentTimeDisplay = document.getElementById("current-time")!;
            const totalTimeDisplay = document.getElementById("total-time")!;
            
            if (audio) {
                timeControl.value = String(audio.currentTime); // Ažurira vrijednost trenutnog vremena
            }

            const currentMinutes = Math.floor(audio!.currentTime / 60);
            const currentSeconds = Math.floor(audio!.currentTime % 60);
            const totalMinutes = Math.floor(audio!.duration / 60);
            const totalSeconds = Math.floor(audio!.duration % 60);
    
            currentTimeDisplay.textContent = `${currentMinutes}:${currentSeconds < 10 ? '0' : ''}${currentSeconds}`;
            totalTimeDisplay.textContent = `${totalMinutes}:${totalSeconds < 10 ? '0' : ''}${totalSeconds}`;
        });

        // Po završetku pjesme, šalje događaj
        audio.addEventListener("ended", () => {
            dispatch('audioEnded');
        });
    });

    // Reaktivno ažuriranje playera kad se 'play' ili 'isPlaying' promijene
    $: if (audio && play) {
        if (audio.src !== play) {
            audio.src = play;  // Postavlja izvor samo kad se promijeni
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
  
<!-- Glavni container za audio player -->
<div class="flex flex-col items-center w-full audio-player">
    <audio id="audio">
        <source src={play}>
        Vaš preglednik ne podržava audio element.
    </audio>

    <!-- Kontrole, dizajnirano kao Spotify -->
    <div class="flex justify-between items-center w-3/4 controls-container">
        <!-- Prikaz trenutnog vremena -->
        <div id="current-time" class="text-gray-600 text-sm time">0:00</div>

        <!-- Kontrola za progresiju -->
        <div class="flex-1 mx-2 progress-container">
            <input type="range" id="progress-bar" class="w-full h-1 bg-gray-300 rounded-lg progress-bar" min="0" max="0" step="1" value="0">
        </div>

        <!-- Prikaz ukupnog vremena -->
        <div id="total-time" class="text-gray-600 text-sm time">0:00</div>

        <!-- Kontrola glasnoće -->
        <input type="range" id="volume-control" class="w-24 h-1 bg-gray-300 rounded-lg volume-control" min="0" max="1" step="0.01" value="1">
    </div>
</div> 
