<template>
  <div>
    <head>
      <meta charset="UTF-8" />
      <title>Sign Up</title>
    </head>
    <body>
      <h1>Sign Up</h1>
      <form @submit.prevent="signUp">
        <label for="email">Email:</label><br />
        <input type="email" id="email" v-model="email" required /><br /><br />

        <label for="username">Username:</label><br />
        <input
          type="text"
          id="username"
          v-model="username"
          required
        /><br /><br />

        <label for="password1">Password:</label><br />
        <input
          type="password"
          id="password1"
          v-model="password1"
          required
        /><br /><br />

        <label for="password2">Confirm Password:</label><br />
        <input
          type="password"
          id="password2"
          v-model="password2"
          required
        /><br /><br />

        <input type="submit" value="Sign Up" />
      </form>
      <p v-if="message">{{ message }}</p>
    </body>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SignupComponent',
  data() {
    return {
      email: '',
      username: '',
      password1: '',
      password2: '',
      message: '',
    };
  },
  methods: {
    async signUp() {
      try {
        const response = await axios.post(
          'http://192.168.1.33:5000/auth/sign-up',
          {
            email: this.email,
            username: this.username,
            password1: this.password1,
            password2: this.password2,
          },
          {
            headers: {
              'Content-Type': 'application/json',
            },
          }
        );

        if (response.data.success) {
          this.message = 'Successfully signed up';
          window.location.href = '/upload';
        } else {
          this.message = response.data.message;
        }
      } catch (error) {
        console.error(error);
        this.message = 'Error signing up';
      }
    },
  },
};
</script>
