<script lang="ts">
    import { onMount } from 'svelte';
    import { hostStore } from '$lib/stores';
    import { goto } from '$app/navigation';
  
    let fileInput: HTMLInputElement; // Explicitly type the fileInput variable
    let name = '';
    let description = '';
    let genre = '';
    let author = '';
  
    
    async function getUser() {
        const user_info = await fetch($hostStore + '/auth/user', {
            method: 'GET',
            credentials: 'include'
        });

        if (user_info.ok) {
            const data = await user_info.json()
            author = data.username
            alert('Continiue');
        } else {
            alert('Log in');
            goto('auth/login')
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
                alert('File uploaded successfully');
            } else if (description.length > 500) {
                alert('File uploaded successfully');
            } else if (genre.length > 30 || genre.length < 1) {
                alert('File uploaded successfully');
            } else if (author.length > 50 || author.length < 1) {
                alert('File uploaded successfully');
            } else {
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                formData.append('name', name);
                formData.append('description', description);
                formData.append('genre', genre);
                formData.append('author', author);
        
                const response = await fetch($hostStore + '/upload', {
                    method: 'POST',
                    body: formData,
                    credentials: 'include',
                });
        
                if (response.ok) {
                    alert('File uploaded successfully');
                } else {
                    const errorData = await response.json();
                    alert(`Error: ${errorData.error}`);
                }
            }
        } else {
            alert('Please select a file to upload.');
        }
    }
  </script>
  
  <!-- File input and upload button -->
  <input type="file" id="file-input" accept="audio/*"/>
  <input type="text" placeholder="Name" bind:value={name}>
  <input type="text" placeholder="Description (optional)" bind:value={description}>
  <input type="text" placeholder="Genre" bind:value={genre}>
  <input type="text" placeholder="Author" bind:value={author}>
  <button on:click={uploadFile}>Upload File</button>
  