<template>
  <div class="profile">
    <h2>Profile</h2>
    <div v-if="user">
      <p><strong>Username: </strong> {{ user.username }}</p>
      <form @submit.prevent="changePassword">
        <div>
          <label class="form-label" for="currentPassword">Current Password:</label>
          <input class="form-control" type="password" id="currentPassword" v-model="currentPassword" required>
        </div>
        <div>
          <label class="form-label" for="newPassword">New Password:</label>
          <input class="form-control" type="password" id="newPassword" v-model="newPassword" required>
        </div>
        <div>
          <label class="form-label" for="confirmPassword">Confirm New Password:</label>
          <input class="form-control" type="password" id="confirmPassword" v-model="confirmPassword" required>
        </div>
        <button class="btn btn-success" type="submit">Change Password</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      user: null,
      currentPassword: '',
      newPassword: '',
      confirmPassword: '',
    };
  },
  async created() {
    try {
      const token = localStorage.getItem('token');
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      };
      const response = await axios.get('/api/profile', config);
      this.user = response.data;
    } catch (error) {
      console.error(error);
      alert('Failed to load profile');
    }
  },
  methods: {
    async changePassword() {
      if (this.newPassword !== this.confirmPassword) {
        alert("New passwords do not match");
        return;
      }
      try {
        const token = localStorage.getItem('token');
        const config = {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        };
        await axios.post('/api/change-password', {
          currentPassword: this.currentPassword,
          newPassword: this.newPassword,
        }, config);
        alert("Password changed successfully");
        this.currentPassword = '';
        this.newPassword = '';
        this.confirmPassword = '';
      } catch (error) {
        console.error(error);
        alert('Failed to change password');
      }
    },
  },
};
</script>

<style scoped>
.profile {
  padding: 20px;
}

h2 {
  color: rgba(8, 60, 44);
}

form {
  margin-top: 20px;
  margin-bottom: 20px;
}

.form-input {
  margin-bottom: 20px;
}

.form-label {
  margin-right: 20px;
  color: rgba(8, 60, 44);
}

.form-control {
  margin-bottom: 10px;
}

.btn {
  background-color: rgba(8, 60, 44);
  color: white;
  margin-bottom: 10px;
}
</style>
