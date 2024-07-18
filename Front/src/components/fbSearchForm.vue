<template>
  <div>
    <div class="card mt-3">
      <div class="card-body">
        <div class="form-group">
          <label for="searchMethod">Search method:</label>
          <select id="searchMethod" v-model="searchMethod" @change="onMethodChange">
            <option disabled value="">Select option</option>
            <option value="profile">Search in user profile</option>
            <option value="keyword">Search by keyword</option>
          </select>
        </div>
        <div v-if="searchMethod === 'profile'" class="form-group">
          <label for="profileLink">Enter Facebook profile link:</label>
          <input id="profileLink" type="text" v-model="profileLink" placeholder="Please enter a valid link" />
          <div class="checkbox-group">
            <label><input type="checkbox" v-model="includeInformation" /> User Information</label>
            <label><input type="checkbox" v-model="includePhotos" /> User Photos</label>
            <label><input type="checkbox" v-model="includePosts" /> User Posts</label>
          </div>
          <div v-if="includePosts" class="additional-options">
            <label for="numPosts">Number of posts:</label>
            <select id="numPosts" v-model="numPosts">
              <option v-for="num in [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]" :key="num" :value="num">{{ num }}</option>
            </select>
            <label for="startDate">Start Date:</label>
            <input id="startDate" type="date" v-model="startDate" />
            <label for="endDate">End Date:</label>
            <input id="endDate" type="date" v-model="endDate" />
          </div>
        </div>
        <div v-if="searchMethod === 'keyword'" class="form-group">
          <label for="keyword">Filter by keyword:</label>
          <input id="keyword" type="text" v-model="keyword" placeholder="Enter keyword" />
        </div>
        <button class="btn btn-success mt-3" @click="onSubmit">Extract</button>
      </div>
    </div>
    <div class="card mt-3">
      <div class="card-body">
        <div class="mt-3">
      <div class="row">
        <div class="col-md-3">
          <p><strong>Results File Name:</strong></p>
          <p>{{ resultsFileName }}</p>
        </div>
        <div class="col-md-3">
          <p><strong>Status:</strong></p>
          <p><span v-if="loading">Loading...</span><span v-else-if="showResults">Success</span><span v-else>Waiting for
              search</span></p>
        </div>
        <div class="col-md-3">
          <label class="form-label">File Format:</label>
          <select class="form-select" v-model="fileFormat">
            <option value="csv">CSV</option>
            <option value="json">JSON</option>
          </select>
        </div>
        <div class="col-md-3">
          <button class="btn btn-success mt-3" @click="downloadFile">Download Results</button>
        </div>
      </div>

        <div class="mt-3" v-if="results && results.length">
          <label class="form-label"><strong>Results:</strong></label>
          <div  class="table-responsive">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th v-for="(value, key) in results[0]" :key="key">{{ key }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(result, index) in results" :key="index">
                  <td v-for="(value, key) in result" :key="key">{{ value }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>
<!-- ------------------------------------------------------------------ -->
<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchMethod: '',
      profileLink: '',
      keyword: '',
      includeInformation: false,
      includePhotos: false,
      includePosts: false,
      numPosts: 5,
      startDate: '',
      endDate: '',
      resultsFileName: '',
      loading: false,
      showResults: false,
      results: [],
      fileFormat: 'csv',
    };
  },
  methods: {
    onMethodChange() {
      this.profileLink = '';
      this.keyword = '';
      this.includeInformation = true;
      this.includePhotos = false;
      this.includePosts = false;
      this.numPosts = 5;
      this.startDate = '';
      this.endDate = '';
    },
    async onSubmit() {
      const token = localStorage.getItem('token');
      const payload = {
        searchMethod: this.searchMethod,
        profileLink: this.profileLink,
        keyword: this.keyword,
        includeInformation: this.includeInformation,
        includePhotos: this.includePhotos,
        includePosts: this.includePosts,
        numPosts: this.numPosts,
        startDate: this.startDate,
        endDate: this.endDate,
      };
      console.log(payload)
      try {
          const response = await axios.post('http://localhost:4000/search/profile', payload,{
            headers: {
            'Authorization': `Bearer ${token}`
          }
        
        });
        this.results=response.data.results;
        this.resultsFileName= response.data.fileName;
        this.showResults = true;
        }
          // console.log(this.posts)
        catch (error) {
        console.log(error);
        this.results = '';
        if(error.message === "Request failed with status code 403"){
          alert(`Please login!`);
        }else{
          alert(`An error occured during the search!`)
        }
        } finally {
        this.loading = false;
        }
      console.log('Form submitted with data:', payload);
      // Call the backend API with the data
    },
    async downloadFile() {
      try
       {
        
        if(this.results.length!=0){
          const file = await axios.get(`http://localhost:4000/download/${this.resultsFileName}`,  {
          params: { fileFormat: this.fileFormat },
          data:{'fileFormat': this.fileFormat},
          responseType: 'blob'
        });
          if (file){
            const url = window.URL.createObjectURL(new Blob([file.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${this.fileName}.${this.fileFormat}`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

        }
        }
       
       
        
      } catch (error) {
        console.error('Error downloading the file:', error);
      }        
    }
    
  },
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-group {
  margin: 15px 0;
  width: 100%;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="date"],
select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: 10px;
}

.table-responsive {
  max-height: 400px;
  overflow-y: auto;
}
</style>
