<script lang="ts">
  import { onMount } from 'svelte';
  import { goto, useData, getUser, loadInfo, page } from '$lib/libraries';
  import global_playlist from '$lib/stores/global_playlist';
  import type { AudioInfo } from '$lib/functions/player';
  import { socket } from "$lib/socket";
  
  let room_audios: number[] = [];
  
  interface AudioItem {
    id: number;
    name: string;
  }
  
  interface ChatRoom {
    host: number;
    audio_ids: number[];
  }
  
  let search = '';
  let quickList: AudioItem[] = [];
  let audioInfos: AudioInfo[] = [];
  let user_id: number;
  let chat: ChatRoom;
  let code: string;
  let song_change = 'add';
  let play_text = 'Play for all';
  
  let messages: { user: string; message: string }[] = [];
  let message = "";
  let user = "guest";
  let host = -1;

  // Funkcija koja se poziva prilikom učitavanja komponente
  onMount(() => {
    // Osiguravamo da imamo korisnika i kod sobe
    getUser(true);
    code = $page.url.pathname.slice(6);
    
    // Učitavanje podataka o korisniku i sobi
    (async () => {
      user_id = await getUser();
      chat = await loadInfo(code, '_ignorename', '/chat/');
      if (!chat) {
        goto('/');
      }
      host = chat.host;
      // Inicijalizacija room_audios i audioInfos
      room_audios = chat.audio_ids;
      audioInfos = await Promise.all(room_audios.map(id => loadInfo(id.toString(), '_ignorename', '/audio/info/')));
    })();
    $global_playlist = [];
    
    // Slušanje dolaznih poruka putem socket-a
    socket.on("message", (data) => {
      messages = [...messages, data];
      
      // Ako je poruka vezana uz promjenu glazbe od ovog korisnika, ne osvježavamo stanje
      if (data.user === user && (data.message === "Added a song" || data.message === "Removed a song")) {
        return;
      }
      (async () => {
        chat = await loadInfo(code, '_ignorename', '/chat/');
        room_audios = chat.audio_ids;
        audioInfos = await Promise.all(room_audios.map(id => loadInfo(id.toString(), '_ignorename', '/audio/info/')));
      })();
    });

    // Slušanje za "play_audio" event
    socket.on("play_audio", (data) => {
      if (data.room === code) {
        // Ažuriranje globalne playlist-e za sve korisnike kada se pokrene audio
        global_playlist.set(data.audioInfos);
      }
    });

    // Pridruživanje chat sobi
    socket.emit("join", { room: code });

    return () => {
      socket.emit("leave", { room: code, id: user_id });
      socket.off("message"); // Čišćenje listenera prilikom uništavanja komponente
      socket.off("play_audio"); // Čišćenje listenera prilikom uništavanja komponente
    };
  });
  
  // Funkcija za slanje poruke u chat
  function sendMessage() {
    if (message.trim()) {
      socket.emit("send_message", { room: code, user, message });
      message = "";
    }
  }
  
  // Funkcija za pretraživanje glazbe
  async function quickSerach() {
    if (search.length > 0) {
      const formData = new FormData();
      formData.append('search', search);
      formData.append('songs_only', 'true');
      formData.append('showPrivate', 'false');
      const response = await useData('/search', 'POST', formData);
      if (response.ok) {
        const data = await response.json();
        quickList = data.audio_files as AudioItem[];
      }
    } else {
      quickList = [];
    }
  }
  
  // Funkcija za pokretanje ili zaustavljanje audio sadržaja
  function play() {
    if (play_text === 'Stop for all') {
      play_text = 'Play for all';
      global_playlist.set([]); // Briše playlistu ako je zaustavljen audio
      socket.emit("play_audio", { room: code, audioInfos: [] });
    } else {
      play_text = 'Stop for all';
      global_playlist.set(audioInfos); // Postavlja playlistu za sve korisnike
      socket.emit("play_audio", { room: code, audioInfos });
    }
  }

  // Funkcija za dodavanje ili uklanjanje audio zapisa
  async function addAudio(change_id: number) {   
    const index = room_audios.indexOf(change_id);

    if (index !== -1) {
      song_change = 'remove';
      message = 'Removed a song';
      room_audios = [...room_audios.slice(0, index), ...room_audios.slice(index + 1)];
    } else {
      song_change = 'add';
      message = 'Added a song';
      room_audios = [...room_audios, change_id];
    }

    audioInfos = await Promise.all(room_audios.map(id => loadInfo(id.toString(), '_ignorename', '/audio/info/')));

    const formData = new FormData();
    formData.append('change_audio', change_id.toString());
    const response = await useData(`/chat/${code}/${song_change}`, 'POST', formData);

    if (response.ok) {
      sendMessage();
    };
  }
</script>
    
<div class="w-full h-1/2 fixed top-0 left-0 -z-10 mt-16 ml-49 rounded-2xl px-6 py-16" style="background: linear-gradient(to bottom, darkolivegreen, #171717);">
  <h1 class="text-7xl mt-1">Chat code: {code}</h1>
  
  <!-- Chat poruke -->
  <div class="absolute left-150 mt-5 overflow-y-auto border border-neutral-300 p-2 bg-black bg-opacity-50 rounded-2xl w-100">
    <div class=" max-h-[100px] overflow-y-auto border border-neutral-300 p-2">
        {#each messages as msg}
            <div><strong>{msg.user}:</strong> {msg.message}</div>
        {/each}
    </div>
    <input type="text" bind:value={message} placeholder="Type a message..." class="mt-2 p-2 w-full rounded-lg bg-neutral-800 text-white border border-neutral-500" />
    <button on:click={sendMessage} class="mt-2 p-2 bg-green-500 rounded-lg text-xs w-full">Send</button>
  </div>

  {#if user_id == host} 
    <!-- Pretraga glazbe za dodavanje u sobu -->
    <input class="bg-neutral-900 rounded mt-5" type="text" placeholder="Search..." bind:value={search} on:input={quickSerach}>

    <!-- Dugme za pokretanje ili zaustavljanje glazbe -->
    <button class="px-4 py-2 bg-green-500 rounded-2xl text-xs absolute mt-3.5 ml-1" on:click={play}>{play_text}</button>

    {#if quickList.length > 0}
    <div class="max-h-60 overflow-y-auto">
      {#each quickList as quick_info}
        <div class="bg-neutral-900 w-100">
          <h6 class=" truncate">{quick_info.name}</h6>
          <button class="px-4 py-2 bg-green-500 rounded-2xl text-xs" on:click={() => addAudio(quick_info.id)}>
            {room_audios.indexOf(quick_info.id) !== -1 ? "-" : "+"}
          </button>         
        </div>
      {/each}
    </div>
    {/if}

    
  {/if}

  <div class="grid grid-cols-3 gap-2 max-h-60 overflow-y-auto w-150 py-3">
    {#if audioInfos.length > 0}
        {#each audioInfos as audioInfo}
            <div class="relative w-40 h-15 border border-neutral-300 bg-neutral-700 flex items-center justify-center rounded">
                <!-- Cijeli pravokutnik je klikabilan -->
                <a href={`/${audioInfo.name.replace(/\s+/g, '-')}_audioid_${audioInfo.id}`} class="absolute inset-0 z-0 flex items-center justify-center text-center">
                    <div class="z-10 text-white text-center px-1 truncate">{audioInfo.name}</div>
                </a>
                
                {#if user_id == host }
                    <!-- Tipka za brisanje; zaustavlja prosljeđivanje klika -->
                    <button class="absolute top-1 right-1 px-2 py-1 bg-red-500 text-xs rounded z-20" on:click={() => addAudio(audioInfo.id)}>
                        -
                    </button>
                {/if}
            </div>
        {/each}
    {/if}
  </div>
  
</div>
