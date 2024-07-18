<template>
  <div class="auth-form">
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
      <div class="form-group">
        <label for="username">Username:</label>
        <input v-model="username" type="text" id="username" class="form-control" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input v-model="password" type="password" id="password" class="form-control" required />
      </div>
      <button type="submit" class="btn btn-secondary">Login</button>
    </form>
  </div>
</template>

<script>
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
    async loginUser() {
      try {
        await this.login({ username: this.username, password: this.password });
        // After successful login, navigate to profile
        this.$router.push('/profile');
      } catch (error) {
        console.error(error);
        alert('Login failed'); // Display login failed message if there's an error
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
