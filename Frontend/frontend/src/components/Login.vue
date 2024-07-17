<template>
  <div>
    <head>
      <meta charset="UTF-8" />
      <title>Login</title>
    </head>
    <body>
      <h1>Login</h1>
      <form @submit.prevent="login">
        <label for="email">Email:</label><br />
        <input type="email" id="email" v-model="email" required /><br /><br />

        <label for="password">Password:</label><br />
        <input
          type="password"
          id="password"
          v-model="password"
          required
        /><br /><br />

        <input type="submit" value="Login" />
      </form>
      <p v-if="message">{{ message }}</p>
    </body>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginComponent',
  data() {
    return {
      email: '',
      password: '',
      message: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post(
          'http://192.168.1.33:5000/auth/login',
          {
            email: this.email,
            password: this.password,
          },
          {
            headers: {
              'Content-Type': 'application/json',
            },
          }
        );
        if (response.data.success) {
          this.message = 'Successfully logged in';
          window.location.href = '/upload'; // Redirect to the home page
        } else {
          this.message = response.data.message;
        }
      } catch (error) {
        console.error(error);
        this.message = 'Error logging in';
      }
    },
  },
};
</script>
