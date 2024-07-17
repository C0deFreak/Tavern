<template>
  <nav>
    <h1>Welcome, {{ username }}</h1>
    <button @click="logout">Logout</button>
  </nav>
  <router-view />
</template>

<style>
#app {
  margin-top: 60px;
}
</style>

<script>
import axios from 'axios';

export default {
  name: 'MyComponent',
  data() {
    return {
      username: '',
    };
  },
  methods: {
    async logout() {
      try {
        const response = await axios.get(
          'http://192.168.1.33:5000/auth/logout'
        );
        if (response.status === 200) {
          window.location.href = '/login';
        } else {
          console.error('Failed to logout');
        }
      } catch (error) {
        console.error('Error during logout:', error);
      }
    },
  },
  async mounted() {
    try {
      const response = await axios.get(
        'http://192.168.1.33:5000/auth/user_info'
      );
      if (response.status === 200) {
        this.username = response.data.username;
        console.log('User info fetched successfully:', response.data);
      } else {
        console.error('Failed to fetch user info');
      }
    } catch (error) {
      console.error('Error fetching user info:', error);
    }
  },
};
</script>
