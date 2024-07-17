<template>
  <div>
    <head>
      <meta charset="UTF-8" />
      <title>Music Library</title>
    </head>
    <body>
      <h1>Upload Music</h1>
      <form @submit.prevent="uploadMusic">
        <label for="name">Name:</label><br />
        <input type="text" id="name" v-model="name" required /><br /><br />

        <label for="genre">Genre:</label><br />
        <input type="text" id="genre" v-model="genre" required /><br /><br />

        <label for="creator">Creator:</label><br />
        <input
          type="text"
          id="creator"
          v-model="creator"
          required
        /><br /><br />

        <label for="audio_file">Choose a file:</label><br />
        <input
          type="file"
          id="audio_file"
          @change="handleFileUpload"
          accept=".wav, .mp3, .ogg"
          required
        /><br /><br />

        <input type="submit" value="Submit" />
      </form>
    </body>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MusicUpload',
  data() {
    return {
      name: '',
      genre: '',
      creator: '',
      audio_file: null,
    };
  },
  methods: {
    handleFileUpload(event) {
      this.audio_file = event.target.files[0];
    },
    async uploadMusic() {
      const formData = new FormData();
      formData.append('name', this.name);
      formData.append('genre', this.genre);
      formData.append('creator', this.creator);
      formData.append('audio_file', this.audio_file);

      try {
        const response = await axios.post(
          'http://192.168.1.33:5000/upload',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          }
        );
        console.log(response.data);
        alert('File successfully uploaded');
        location.reload();
      } catch (error) {
        console.error(error);
        alert('Error uploading file');
      }
    },
  },
};
</script>
