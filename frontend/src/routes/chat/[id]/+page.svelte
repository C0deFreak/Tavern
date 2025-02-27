<script lang="ts">
    import { onMount } from 'svelte';
    import { goto, useData, getUser, loadInfo, page } from '$lib/libraries';
    import global_playlist from '$lib/stores/global_playlist';
    import type { AudioInfo } from '$lib/functions/player';
    import { socket } from "$lib/socket";
  import { redirect } from '@sveltejs/kit';
    
    let private_playlist = false;
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
    
    let messages: { user: string; message: string }[] = [];
    let message = "";
    let user = "Guest";
    
    onMount(() => {
        // Ensure we have the user and room code
        getUser(true);
        code = $page.url.pathname.slice(6);
        console.log("Room code:", code);
        
        // Load user and chat room information asynchronously
        (async () => {
            user_id = await getUser();
            chat = await loadInfo(code, '_ignorename', '/chat/');
            console.log("Chat info:", chat);
            // Initialize room_audios and audioInfos
            room_audios = chat.audio_ids;
            audioInfos = await Promise.all(room_audios.map(id => loadInfo(id.toString(), '_ignorename', '/audio/info/')));
        })();
        
        // Listen for incoming socket messages
        socket.on("message", (data) => {
            console.log("Received socket message:", data);
            messages = [...messages, data];
            // If this message is an audio add/remove from this user, skip refreshing state
            if (data.user === user && (data.message === "Added a song" || data.message === "Removed a song")) {
                return;
            }
            (async () => {
                chat = await loadInfo(code, '_ignorename', '/chat/');
                room_audios = chat.audio_ids;
                audioInfos = await Promise.all(room_audios.map(id => loadInfo(id.toString(), '_ignorename', '/audio/info/')));
            })();
        });

        
        // Join the room
        socket.emit("join", { room: code });
        console.log("Joined room:", code);
        
        return () => {
            socket.emit("leave", { room: code });
            socket.off("message"); // Cleanup listener on component destroy
        };
    });
    
    function sendMessage() {
      if (message.trim()) {
        console.log("Sending message:", message);
        socket.emit("send_message", { room: code, user, message });
        message = "";
      }
    }
    
    async function quickSerach() {
      if (search.length > 0) {
        const formData = new FormData();
        formData.append('search', search);
        formData.append('showPrivate', private_playlist.toString());
        const response = await useData('/search', 'POST', formData);
        if (response.ok) {
          const data = await response.json();
          quickList = data.audio_files as AudioItem[];
        }
      } else {
        quickList = [];
      }
    }
    
    function play() {
      console.log("Playing audioInfos:", audioInfos);
      global_playlist.set(audioInfos);
      console.log("Global playlist updated:", global_playlist);
    }
    
    async function addAudio(change_id: number) {   
        const index = room_audios.indexOf(change_id);
        console.log("Current room_audios:", room_audios);

        if (index !== -1) {
            song_change = 'remove';
            message = 'Removed a song';
            room_audios = [...room_audios.slice(0, index), ...room_audios.slice(index + 1)];
        } else {
            song_change = 'add';
            message = 'Added a song';
            room_audios = [...room_audios, change_id];
        }

        console.log("Song change:", song_change);
        audioInfos = await Promise.all(room_audios.map(id => loadInfo(id.toString(), '_ignorename', '/audio/info/')));
        console.log("Updated audioInfos:", audioInfos);

        const formData = new FormData();
        formData.append('change_audio', change_id.toString());
        const response = await useData(`/chat/${code}/${song_change}`, 'POST', formData);

        if (!response.ok) {
            console.error("Error updating backend:", response.status);
        } else {
            sendMessage()
        }
    }

  </script>
    
  <div class="w-full h-1/2 fixed top-0 left-0 -z-10 mt-16 ml-49 rounded-2xl px-6 py-16" style="background: linear-gradient(to bottom, darkolivegreen, #171717);">
    <h1 class="text-9xl">{code}</h1>
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="text" placeholder="Search..." bind:value={search} on:input={quickSerach}>
    
    {#if quickList.length > 0}
      {#each quickList as quick_info}
        <div class="bg-neutral-900">
          <h6>{quick_info.name}</h6>
          <button class="px-4 py-2 bg-green-500 rounded-2xl text-xs" on:click={() => addAudio(quick_info.id)}>
            {room_audios.indexOf(quick_info.id) !== -1 ? "-" : "+"}
          </button>         
        </div>
      {/each}
    {/if}
    
    <button class="px-4 py-2 bg-green-500 rounded-2xl text-xs" on:click={play}>Play</button>
    
    {#if room_audios.length > 0}
      {#each audioInfos as audioInfo}
        <div>
          <a href={`/${audioInfo.name.replace(/\s+/g, '-')}_audioid_${audioInfo.id}`}>
            <button class="bg-neutral-700 py-1 px-2 border border-neutral-300 text-s mb-2">{audioInfo.name}</button> 
          </a>   
          {#if user_id == chat.host} 
            <button class="px-2 py-1 bg-red-500 text-xs rounded" on:click={() => addAudio(audioInfo.id)}>-</button> 
          {/if}      
        </div>
      {/each}
    {/if}
    
    <h1>Chat Room: {code}</h1>
    <div class="chat-box">
      {#each messages as msg}
        <div><strong>{msg.user}:</strong> {msg.message}</div>
      {/each}
    </div>
    <input type="text" bind:value={message} placeholder="Type a message..." />
    <button on:click={sendMessage}>Send</button>
  </div>
    
  <style>
    .chat-box {
      max-height: 300px;
      overflow-y: auto;
      border: 1px solid #ccc;
      padding: 10px;
    }
  </style>
  