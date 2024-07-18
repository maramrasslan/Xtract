<!-- src/views/Search.vue -->
<template>
  <header>
    <img src="../assets/img/twitter.png" height="100px" width="100px">
    <div class="name"> 
      <h1>Twitter </h1>
    </div>
  </header>
  <SearchForm />
</template>

<script>
import SearchForm from '../components/SearchForm.vue';

export default {
  name: 'SearchTwitter',
  components: {
    SearchForm,
  },
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