<template>
  <div class="auth-form">
    <h2>Sign Up</h2>
    <form @submit.prevent="signupUser">
      <div class="form-group">
        <label for="username">Username:</label>
        <input v-model="username" type="text" id="username" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input v-model="password" type="password" id="password" class="form-control" required />
      </div>
      <button type="submit" class="btn btn-secondary">Sign Up</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    ...mapActions(['login']),
    async signupUser() {
      try {
        const response = await axios.post('/api/signup', {
          username: this.username,
          password: this.password,
        });

        alert(response.data.message); // Display successful message
        await this.login({ username: this.username, password: this.password });
        this.$router.push('/profile'); // Redirect to profile page after signup
      } catch (error) {
        console.error(error);
        alert('Sign up failed'); // Display signup failed message if there's an error
      }
    },
  },
};
</script>

<style scoped>
.auth-form {
  max-width: 500px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
}
.btn {
  background-color: #083C2C !important;
  color: white;
  margin-top: 2%;
}
</style>