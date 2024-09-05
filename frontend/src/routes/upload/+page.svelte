<script lang="ts">
    import { onMount } from 'svelte';
    import { hostStore } from '$lib/stores';

    let fileInput: HTMLInputElement; // Explicitly type the fileInput variable

    onMount(() => {
        // Ensure the fileInput element is correctly assigned
        fileInput = document.querySelector('#file-input') as HTMLInputElement;
    });

    async function uploadFile() {
        if (fileInput.files?.length) {
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);

            await fetch($hostStore + '/upload', {
                method: 'POST',
                body: formData,
            });
        }

    }
</script>

<!-- File input and upload button -->
<input type="file" id="file-input" accept="audio/*"/>
<button on:click={uploadFile}>Upload File</button>
