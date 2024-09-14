<script lang="ts">
    import { onMount } from 'svelte';
    import { hostStore } from '$lib/stores';
    import { goto } from '$app/navigation';
  
    let fileInput: HTMLInputElement; // Explicitly type the fileInput variable
    let name = '';
    let description = '';
    let genre = '';
    let author = '';
    let private_audio = false;

    let specialChars =/[`%^_*()\+=\[\]{};\\|<>\/?~]/
  
    
    async function getUser() {
        const user_info = await fetch($hostStore + '/auth/user', {
            method: 'GET',
            credentials: 'include'
        });

        if (user_info.ok) {
            const data = await user_info.json()
            author = data.username
        } else {
            goto('/auth/login')
        }
    }
  
    onMount(() => {
      getUser();
      fileInput = document.querySelector('#file-input') as HTMLInputElement;
    });
  
    // Upload file and metadata (name, description, genre, author)
    async function uploadFile() {
        if (fileInput.files?.length) {
            if (name.length > 100 || name.length < 1) {
                goto('/upload');
            } else if (description.length > 500) {
                goto('/upload');
            } else if (genre.length > 30 || genre.length < 1) {
                goto('/upload');
            } else if (author.length > 50 || author.length < 1) {
                goto('/upload');
            } else if (specialChars.test(name)) {
                goto('/upload');
            } else {
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                formData.append('name', name);
                formData.append('description', description);
                formData.append('genre', genre);
                formData.append('author', author);
                formData.append('private', private_audio.toString());
        
                const response = await fetch($hostStore + '/upload', {
                    method: 'POST',
                    body: formData,
                    credentials: 'include',
                });
        
                goto('/');
            }
        }
    }
  </script>
  
  <!-- File input and upload button -->
  <input type="checkbox" placeholder="Private?" bind:checked={private_audio}>
  <input type="file" id="file-input" accept="audio/*"/>
  <input type="text" placeholder="Name" bind:value={name}>
  <input type="text" placeholder="Description (optional)" bind:value={description}>
  <input type="text" placeholder="Genre" bind:value={genre}>
  <input type="text" placeholder="Author" bind:value={author}>
  <button on:click={uploadFile}>Upload File</button>
  