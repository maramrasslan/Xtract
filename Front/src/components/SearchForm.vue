<template>
  <div>
    <div class="card mt-3">
      <div class="card-body">
        <form @submit.prevent="search">
          <div class="mb-3">
            <label class="form-label">Search Method:</label>
            <select class="form-select" v-model="searchMethod">
              <option value="Search in user profile">Search in user profile</option>
              <option value="Search by keyword">Search by keyword</option>
            </select>
          </div>
          <div v-if="searchMethod === 'Search in user profile'" class="mb-3">
            <label class="form-label">Username:</label>
            <input class="form-control" v-model="username" type="text" />
          </div>
          <div class="mb-3">
            <label class="form-label">Keyword:</label>
            <input class="form-control" v-model="keyword" type="text" />
          </div>
          <div class="mb-3">
            <label class="form-label">Loop Limit:</label>
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
          <button class="btn btn-success" type="submit" :disabled="loading">Search</button>
        </form>
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
          <label class="download-label">Download</label>
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

<script>
import axios from 'axios';

export default {
  name: 'SearchForm',
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
      loading: false,
      showResults: false,
      resultsFileName: '',
      fileFormat: 'csv',
      results: [],
    };
  },
  methods: {
    async search() {
      this.loading = true;
      this.showResults = false;
      this.results = [];
      this.resultsFileName = '';
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
      };

      try {
        const response = await axios.post('/api/search', payload, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        this.results = response.data.results;
        this.resultsFileName = response.data.fileName;
        this.showResults = true;
      } catch (error) {
        console.error(error);
        this.results = 'An error occurred during the search.';
      } finally {
        this.loading = false;
      }
    },
    async downloadFile() {
      try {
        const response = await axios.get(`/api/download/${this.resultsFileName}`, {
          params: { fileFormat: this.fileFormat },
          responseType: 'blob',
        });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `${this.resultsFileName}.${this.fileFormat}`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } catch (error) {
        console.error('Error downloading the file:', error);
      }
    },
  },
};
</script>

<style scoped>
.card {
  margin-top: 20px;
}

.form-label {
  color: rgba(8, 60, 44);
}
.mt-3 {
  margin-bottom: 30px;
}
.btn {
  background-color: rgba(8, 60, 44);
  color: white;
  margin-left: 10px;
}

.result-box {
  width: 100%;
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #ccc;
  padding: 10px;
  white-space: pre-wrap;
  background-color: #f9f9f9;
}

.table-responsive {
  max-height: 400px;
  overflow-y: auto;
}
</style>
