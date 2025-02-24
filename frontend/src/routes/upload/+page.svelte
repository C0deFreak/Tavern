<script lang="ts">
    import { onMount, goto, useData, getUser } from '$lib/libraries'

  
    let fileInput: HTMLInputElement; // Explicitly type the fileInput variable
    let name = '';
    let description = '';
    let genre = '';
    let private_audio = false;
    let terms = false;

    let specialChars =/[`%^_*()\+=\[\]{};\\|<>\/?~]/

  
    onMount(async () => {
        getUser(true);
        fileInput = document.querySelector('#file-input') as HTMLInputElement;
    });
  
    // Upload file and metadata (name, description, genre, author)
    async function uploadFile() {
        if (fileInput.files?.length && terms) {
            if (name.length > 100 || name.length < 1) {
                goto('/upload');
            } else if (description.length > 500) {
                goto('/upload');
            } else if (genre.length > 30 || genre.length < 1) {
                goto('/upload');
            } else if (specialChars.test(name)) {
                goto('/upload');
            } else {
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                formData.append('name', name);
                formData.append('description', description);
                formData.append('genre', genre);
                formData.append('private', private_audio.toString());
                
                const response = await useData('/audio/upload', 'POST', formData);

                if (response.ok) {
                    goto('/');
                }
            }
        }
    }
</script>

<div class="w-full h-1/2 fixed top-0 left-0 -z-10 mt-16 ml-49 rounded-2xl px-6 py-16" style="background: linear-gradient(to bottom, darkolivegreen, #171717);">
    <!-- File input and upload button -->
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="file" id="file-input" accept="audio/*"/>
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="text" placeholder="Name" bind:value={name}>
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="text" placeholder="Description (optional)" bind:value={description}>
    <input class="bg-neutral-900 rounded py-2 px-2 mt-2" type="text" placeholder="Genre" bind:value={genre}>
    <br>
    <p>Upload privately?</p>
    <input type="checkbox" bind:checked={private_audio}>
    <br>
    <p>I agree to <a href="/terms-and-conditions">Terms and conditions</a></p>
    <input type="checkbox" bind:checked={terms}>
    <br>
    <button class="px-4 py-2 bg-green-500 rounded-2xl text-xs" on:click={uploadFile}>Upload File</button>
</div>
  