<template>
    <header>
      <img src="../assets/img/facebook.png" height="100px" width="100px">
      <div class="name"> 
        <h1>Facebook </h1>
      </div>
    </header>
    <fbSearchForm />
</template>
  
<script>
import fbSearchForm from '../components/fbSearchForm.vue';

export default {
    name: 'SearchFacebook',
    components: {
        fbSearchForm,
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
  margin-left: -2%;
  font-family: 'Montserrat'
}
</style>