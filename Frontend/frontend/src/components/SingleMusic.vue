<template>
  <div>
    <head>
      <meta charset="UTF-8" />
      <title>Music Library</title>
    </head>
    <body>
      <div v-if="loading">Loading...</div>
      <div v-else>
        <h1>{{ music.name }}</h1>
        <h3>{{ music.creator }} - {{ music.genre }}</h3>
        <audio controls v-if="music.audio_file">
          <source
            :src="'http://localhost:5000/music_upload/' + music.audio_file"
            :type="'audio/' + music.audio_file.split('.').pop()"
          />
        </audio>
      </div>
    </body>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SingleMusic',
  data() {
    return {
      music: {}, // Initialize as an object
      loading: true, // Initialize loading state
    };
  },
  methods: {
    getMusic() {
      const id = this.$route.params.id;
      const name = this.$route.params.name;
      const path = `http://localhost:5000/music/${name}_${id}`;
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          this.music = res.data; // Assign the response data to music
          this.loading = false; // Set loading to false once data is fetched
        })
        .catch((err) => {
          console.error(err);
          this.loading = false; // Set loading to false in case of an error
        });
    },
  },
  created() {
    this.getMusic();
  },
};
</script>
