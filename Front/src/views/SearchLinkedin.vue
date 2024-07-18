<!-- src/views/Search.vue -->
<template>
  <header>
    <img src="../assets/img/linkedin.png" height="100px" width="100px">
    <div class="name"> 
      <h1>Linkedin </h1>
    </div>
  </header>
  <SearchFormLinkedin />
</template>

<script>
import SearchFormLinkedin from '../components/SearchFormLinkedin.vue';

export default {
  name: 'SearchLinkedin',
  components: {
    SearchFormLinkedin,
  }
};
</script>

<style scoped>
header {
  display: flex;
  
  margin-top: 10px;
  justify-content: center;
  padding: 20px 0;
  color: white;
}
.name{
display: flex;
align-items: left;
margin-top: 50px;
margin-left: 0%;
font-family: 'Montserrat'
}
</style>
  