<template>
  <div class="history">
    <h2>Search History</h2>
    <div v-if="searchHistory.length > 0">
      <table>
        <thead>
          <tr>
            <th>App</th>
            <th>Query</th>
            <th>Search Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(history, index) in searchHistory" :key="index">
            <td>{{ history.service }}</td>
            <td>{{ history.query }}</td>
            <td>{{ history.date }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>No search history found.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchHistory: [],
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
      const response = await axios.get('/api/history', config);
      this.searchHistory = response.data;
    } catch (error) {
      console.error(error);
      alert('Failed to load search history');
    }
  },
};
</script>

<style scoped>

h2 {
  color: rgba(8, 60, 44);
}

.history {
  padding: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 30px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
  color:black;
}

th {
  background-color: #f2f2f2;
}
</style>
