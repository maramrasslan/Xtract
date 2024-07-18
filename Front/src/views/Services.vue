<!-- src/views/Services.vue -->
<template>
  <div class="container">
    <div class="services">
      <div class="search-profile">
        <router-link to="/searchProfile" custom v-slot="{ navigate }">
          <button class="search-profile-display" @click="navigate">
            Cross-platform profile search
          </button>
        </router-link>
      </div>
      <div class="search-twitter">
        <router-link to="/searchTwitter" custom v-slot="{ navigate }">
          <button class="search-twitter-display" @click="navigate">
            Twitter Search
          </button>
        </router-link>
      </div>
      <div class="search-facebook">
        <router-link to="/searchFacebook" custom v-slot="{ navigate }">
          <button class="search-facebook-display" @click="navigate">
            Facebook Search
          </button>
        </router-link>
      </div>
      <div class="search-linkedin">
        <router-link to="/searchLinkedin" custom v-slot="{ navigate }">
          <button class="search-linkedin-display" @click="navigate">
            Linkedin Search
          </button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Services',
};
</script>

<style scoped>
/* Add font imports */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Merriweather:ital,wght@0,400;0,700;1,400;1,700&display=swap');

/* Update typography styles */
.container {
  margin-top: 20px;
  font-family: 'Merriweather', serif; /* set font family for body text */
}

.services {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-gap: 25px;
  padding: 20px;
}

.search-twitter,
.search-facebook,
.search-linkedin,
.search-profile {
  display: flex;
  height: 100px;
}

.search-profile-display {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80%;
  border-radius: 10px;
  border: 0;
  background-image: radial-gradient(#255D4C,  #A6B2AE);
  color: white;
  padding-left: 20px;
  font-size: 20px;
  font-family: 'Montserrat', sans-serif; /* set font family for headings */
  cursor: pointer;
}
.search-twitter-display {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80%;
  border-radius: 10px;
  border: 0;
  background-image: radial-gradient(#000000 0%, #111010, #3c4441 100%);
  color: white;
  padding-left: 20px;
  font-size: 20px;
  font-family: 'Montserrat', sans-serif; /* set font family for headings */
  cursor: pointer;
}

.search-twitter-display img {
  margin-left: 80px;
  width: 50px;
  height: 50px;
}

.search-facebook-display {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80%;
  border-radius: 10px;
  border: 0;
  background-image: radial-gradient(#052c6c 0%, #254d8f, #547bb9 100%);
  color: white;
  padding-left: 20px;
  font-size: 20px;
  font-family: 'Montserrat', sans-serif; /* set font family for headings */
  cursor: pointer;
}

.search-facebook-display img {
  margin-left: 80px;
  width: 50px;
  height: 50px;
}

.search-linkedin-display {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80%;
  border-radius: 10px;
  border: 0;
  background-image: radial-gradient(#007ebb, #4394b6, #6ca4b9 100%);
  color: white;
  padding-left: 20px;
  font-size: 20px;
  font-family: 'Montserrat', sans-serif; /* set font family for headings */
  cursor: pointer;
  height: 100px
}

.search-linkedin-display img {
  margin-left: 80px;
  width: 50px;
  height: 50px;
}

.search-profile-display {
  width: 80%;
  border-radius: 10px;
  border: 0;
  font-family: 'Montserrat', sans-serif; /* set font family for headings */
}
</style>