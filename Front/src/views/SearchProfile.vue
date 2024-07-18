<template>
  <div class="container">
    <h2>Find profiles across different platforms</h2>
    <form @submit.prevent="searchProfile">
      <div class="form-input">
        <label class="form-label" for="profileName">Profile Name:</label>
        <input class="form-control" type="text" id="profileName" v-model="profileName" required />
      </div>
      <button class="btn btn-success" type="submit" :disabled="loading">Search</button>
      <p><span v-if="loading">Loading...</span></p>
    </form>
    
    <div v-if="profiles.length > 0 || linkedin.length > 0 || facebook.length > 0">
      <h3>Results:</h3>
      <div v-for="profile in profiles" :key="profile.ProfileLink" class="profile">
        <p>Twitter account: </p> 
        <img :src="profile.ProfileImg" alt="Profile Image" />
        <a :href="profile.ProfileLink" target="_blank">{{ profile.ProfileLink }}</a>
      </div>

      <div v-for="profile in linkedin" :key="profile.ProfileLink" class="profile">
        <p>Linkedin account: <strong> {{ profile.ProfileName }}</strong> </p> 
        <img :src="profile.ProfileImg" alt="Profile Image" />
        <a :href="profile.ProfileLink" target="_blank">{{ profile.ProfileLink }}</a>
      </div>

      <div v-for="profile in facebook" :key="profile.ProfileLink" class="profile">
        <p>Facebook account: </p> 
        <img :src="profile.ProfilePhoto" alt="Profile Image" />
        <a :href="profile.ProfileLink" target="_blank">{{ profile.ProfileLink }}</a>
      </div>
    
    </div>
    
    <div v-else-if="searched">
      <p>No profiles found.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SearchProfile',
  data() {
    return {
      profileName: '',
      profiles: [],
      searched: false,
      loading: false,
      linkedin:[],
      facebook:[]
    };
  },
  methods: {
    async searchProfile() {
      try {
        this.loading = true;
        const response = await axios.post('/api/findProfile', {
          profileName: this.profileName
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        const linkedin_response = await axios.post('http://localhost:5000/findProfile', {
          profileName: this.profileName
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        const facebook_response = await axios.post('http://localhost:4000/findFBProfile', {
          profileName: this.profileName
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });

        this.profiles = response.data.results;
        this.linkedin = linkedin_response.data.profiles;
        this.facebook = facebook_response.data.profiles;
        this.searched = true;
      } catch (error) {
        console.error('Error searching profile:', error);
        this.profiles = [];
        this.linkedin = [];
        this.facebook = [];
        this.searched = true;
      }finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.container {
  margin-top: 20px;
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

.profile {
  margin-top: 30px;
  margin-bottom: 10px;
}

.profile img {
  width: 50px;
  height: 50px;
  margin-left: 20px;
  margin-right: 30px;
  vertical-align: middle;
}
</style>
