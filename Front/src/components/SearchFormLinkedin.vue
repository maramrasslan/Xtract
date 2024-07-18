<!-- src/components/SearchForm.vue -->
<template>
  <div>
    <div class="card mt-3">
      <div class="card-body">
        <form @submit.prevent="SearchLinkedin">
          <div class="mb-3">
            <label class="form-label">Search Method:</label>
            <select class="form-select" v-model="searchMethod">
              <option value="Search in user profile">Search in user profile</option>
              <option value="Search by keyword">Search by keyword</option>
            </select>
          </div>
          <div v-if="searchMethod === 'Search in user profile'" class="mb-3">
            <label class="form-label">Enter Linkedin Username:</label>
            <input class="form-control" v-model="username" type="text" />
          </div>
          <div v-if="searchMethod === 'Search in user profile'" class="mb-3">
            <span style="color:lightgrey">Include:</span>
            <input class="checkbox" v-model="filters['name']" type="checkbox" >
            <label>Name</label>
            <input class="checkbox" v-model="filters['subtitle']" type="checkbox" >
            <label>Subtitle</label>
            <input class="checkbox" v-model="filters['about']" type="checkbox" >
            <label>About</label>
            <input class="checkbox" v-model="filters['experience']" type="checkbox" >
            <label>Experience</label>
            <input class="checkbox" v-model="filters['education']" type="checkbox">
            <label>Education</label>
            <input class="checkbox" v-model="filters['posts']" type="checkbox">
            <label>Posts</label>
          </div>
          <div class="mb-3">
            <label class="form-label">Filter by Keyword:</label>
            <input class="form-control" v-model="keyword" type="text" />
          </div>
          <div class="mb-3">
            <label class="form-label">No. of results:</label>
            <input class="form-control" v-model="loopLimit" type="number" />
          </div>
          <div class="mb-3">
            <label class="form-label">Start Date:</label>
            <input class="form-control" v-model="startDate" type="date" />
          </div>
          <div class="mb-3">
            <label class="form-label">End Date:</label>
            <input class="form-control" v-model="endDate" type="date" />
          </div>
          <div class="mb-3">
            <label class="form-label">Start Time:</label>
            <input class="form-control" v-model="startTime" type="time" />
          </div>
          <div class="mb-3">
            <label class="form-label">End Time:</label>
            <input class="form-control" v-model="endTime" type="time" />
          </div>
          <button class="btn" type="submit">Search</button>
        </form>
      </div>
    </div>
      <div class="mt-3">
      <div class="row">
        <div class="col-md-3">
          <p><strong>Results File Name:</strong></p>
          <p v-if="Object.keys(profile).length!=0">{{ profileFileName }}</p>
          <p v-if="filters.posts">{{ postsFileName }}</p>
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
          <button class="btn btn-success mt-3" @click="downloadFile">Download</button>
        </div>
      </div>  
    </div>
  </div> 
  <!-- --------------------PROFILE---------------------------------------->
  <div class="mt-3" v-if="profile">
    <p style="color:#00674f;font-size:xx-large">RESULTS</p>
        <label v-if="Object.keys(profile).length!=0" style="font-size: x-large;" ><strong>Profile Info:</strong></label>
        <div  class="table-responsive">
          <div v-if="filters.name && profile.name ">
            <div class="profile-attr">Name:</div>
            <div class="profile-val">{{ profile.name}}</div>
          </div>
          <div v-if="filters.subtitle && profile.subtitle ">
            <div class="profile-attr">Subtitle:</div>
            <div class="profile-val">{{ profile.subtitle }}</div>
          </div>
          <div v-if="filters.about && profile.about ">
            <div class="profile-attr">About:</div>
            <div class="profile-val">{{ profile.about }}</div>
          </div>
          <div v-if="filters.experience && profile.experience ">
            <div class="profile-attr">Experience:</div>
            <div class="profile-val">{{ profile.experience }}</div>
          </div>
          <div v-if="filters.education && profile.education ">
            <div class="profile-attr">Education:</div>
            <div class="profile-val">{{ profile.education }}</div>
          </div>
        </div>
      </div>
  <!-- --------------------POSTS----------------------------------->
  <div class="mt-3" v-if="filters.posts && posts.length > 0 ">
        <label v-if="posts.length!=0" style="font-size: x-large;" ><strong>Posts:</strong></label>
        <div  class="table-responsive">
          <table class="table table-bordered">
            <thead>
              <tr>
                <th v-for="(value, key) in posts[0]" :key="key">{{ key }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(post, index) in posts" :key="index">
                <td v-for="(value, key) in post" :key="key">{{ value }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
   
  
    
</template>
  
<script>
  import axios from 'axios';
  
  export default {
    name: 'SearchFormLinkedin',
    data() {
      return {
        searchMethod: 'Search in user profile',
        username: '',
        keyword: '',
        loopLimit: 10,
        startDate: '',
        endDate: '',
        startTime: '',
        endTime: '',
        filters:{
            'name':true,
            'subtitle':true,
            'about':true,
            'experience':true,
            'education':true,
            'posts':true
        },
        loading: false,
        showResults: false,
        resultsFileName: '',
        fileFormat: 'csv',
        error:'',
        // results: [],
        posts:[],
        profile:{},
        profileFileName:'',
        postsFileName:'',

      };
    },
    methods: {
      async SearchLinkedin() {
        this.loading = true;
        this.showResults = false;
        // this.results = [];
        this.profileFileName = '';
        this.postsFileName = '';
        this.profile={};
        const token = localStorage.getItem('token');
        const payload = {
          searchMethod: this.searchMethod,
          username: this.username,
          keyword: this.keyword,
          loopLimit: this.loopLimit,
          startDate: this.startDate,
          endDate: this.endDate,
          startTime: this.startTime,
          endTime: this.endTime,
          filters:this.filters,
        };
  
        // console.log(this.searchMethod)
        try {
          const response = await axios.post('http://localhost:5000/searchLinkedin', payload,{
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        if (this.searchMethod === "Search in user profile"){
          this.profile = response.data.profile;
          if (Object.keys(this.profile).length!=0){
            this.profileFileName = response.data.profilefileName;
          }
          if (this.filters['posts']){
            this.posts = response.data.posts;
            this.postsFileName = response.data.postsfileName;
          }
        }
        else {
          this.posts = response.data.posts;
          this.postsFileName = response.data.postsfileName;
        }
         
          // console.log(this.posts)
          this.showResults = true;
        } catch (error) {
        console.log(error);
        // this.results = '';
        if(error.message === "Request failed with status code 403"){
          alert(`Please login!`);
        }else{
          alert(`An error occured during the search!`)
        }
        } finally {
        this.loading = false;
        }
      },
      async downloadFile() {
      try
       {
        
        if(Object.keys(this.profile).length!=0){
          const profileFile = await axios.get(`http://localhost:5000/download/${this.profileFileName}`,  {
          params: { fileFormat: this.fileFormat },
          data:{'fileFormat': this.fileFormat},
          responseType: 'blob'
        });
          if (profileFile){
            const profileUrl = window.URL.createObjectURL(new Blob([profileFile.data]));
            const profileLink = document.createElement('a');
            profileLink.href = profileUrl;
            profileLink.setAttribute('download', `${this.profileFileName}.${this.fileFormat}`);
            document.body.appendChild(profileLink);
            profileLink.click();
            document.body.removeChild(profileLink);

        }
        }
        if (this.filters['posts']){
          const postsFile = await axios.get(`http://localhost:5000/download/${this.postsFileName}`, {
          params: { fileFormat: this.fileFormat },
          data:{'fileFormat': this.fileFormat},
          responseType: 'blob',
        });
          if(postsFile){
            const postsUrl = window.URL.createObjectURL(new Blob([postsFile.data]));
            const postsLink = document.createElement('a');
            postsLink.href = postsUrl;
            postsLink.setAttribute('download', `${this.postsFileName}.${this.fileFormat}`);
            document.body.appendChild(postsLink);
            postsLink.click();
            document.body.removeChild(postsLink);
          }
       
        }
      } catch (error) {
        console.error('Error downloading the file:', error);
      }        
    }
    },
  }
  </script>
  
  <style scoped>
  .card {
    margin-top: 20px;
  }
  .form-label{
    color: rgba(8,60,44);
  }
  .btn{
    background-color: rgba(8,60,44);
    color: white;
    margin-left: 10px;
  }
  .checkbox{
    margin-left: 8px;

  }

  .profile-attr {
    font-size: large;
    color: #00674f;
    font-weight: bold;
    font-family:  Verdana, Geneva, Tahoma, sans-serif;
    margin:3px
  }

  .profile-val{
    /* font-weight: bold; */
    font-family: Verdana, Geneva, Tahoma, sans-serif;
    margin:3px;
    
  }
  </style>
  