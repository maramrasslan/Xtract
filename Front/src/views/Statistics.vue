<template>
    <div class="statistics">
        <h2>Statistics</h2>
        <div v-if="loading">Loading...</div>
        <div v-else>
            <div class="chart-container">
                <h3>Total Searches</h3>
                <p>{{ totalSearches }}</p>
            </div>

            <div class="chart-container">
                <h3>Searches Per User</h3>
                <BarChart :chart-data="searchesPerUserData" />
            </div>

            <div class="chart-container">
                <h3>Searches Over Time</h3>
                <LineChart :chart-data="searchesOverTimeData" />
            </div>

            <div class="chart-container">
                <h3>Average Search Duration</h3>
                <p>{{ averageSearchDuration }} ms</p>
            </div>

            <div v-if="userSearchesOverTimeData.labels.length > 0" class="chart-container">
                <h3>Your Searches Over Time</h3>
                <LineChart :chart-data="userSearchesOverTimeData" />
            </div>
        </div>
    </div>
</template>

<script>
import { defineComponent, reactive, onMounted } from 'vue';
import { BarChart, LineChart } from 'vue-chart-3';
import axios from 'axios';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default defineComponent({
    components: {
        BarChart,
        LineChart,
    },
    setup() {
        const state = reactive({
            loading: true,
            totalSearches: 0,
            searchesPerUserData: {
                labels: [],
                datasets: [{ label: 'Searches Per User', data: [] }],
            },
            searchesOverTimeData: {
                labels: [],
                datasets: [{ label: 'Searches Over Time', data: [] }],
            },
            averageSearchDuration: 0,
            userSearchesOverTimeData: {
                labels: [],
                datasets: [{ label: 'Your Searches Over Time', data: [] }],
            },
        });

        onMounted(async () => {
            try {
                const token = localStorage.getItem('token');
                const config = {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                };

                const [
                    totalSearchesResponse,
                    searchesPerUserResponse,
                    searchesOverTimeResponse,
                    averageSearchDurationResponse,
                    userSearchesOverTimeResponse,
                ] = await Promise.all([
                    axios.get('/api/statistics/total-searches', config),
                    axios.get('/api/statistics/searches-per-user', config),
                    axios.get('/api/statistics/searches-over-time', config),
                    axios.get('/api/statistics/average-search-duration', config),
                    axios.get('/api/statistics/user-searches-over-time', config),
                ]);

                state.totalSearches = totalSearchesResponse.data.totalSearches;

                const totalSearches = searchesPerUserResponse.data.reduce((total, user) => total + user.count, 0);
                const averageSearchesPerUser = totalSearches / searchesPerUserResponse.data.length;

                state.searchesPerUserData.labels = ['Average'];
                state.searchesPerUserData.datasets[0].data = [averageSearchesPerUser];

                state.searchesOverTimeData.labels = searchesOverTimeResponse.data.map(item => item._id);
                state.searchesOverTimeData.datasets[0].data = searchesOverTimeResponse.data.map(item => item.count);

                state.averageSearchDuration = averageSearchDurationResponse.data?.avgDuration
                    ? averageSearchDurationResponse.data.avgDuration.toFixed(2)
                    : 'N/A';

                if (userSearchesOverTimeResponse.data.length > 0) {
                    state.userSearchesOverTimeData.labels = userSearchesOverTimeResponse.data.map(item => item._id);
                    state.userSearchesOverTimeData.datasets[0].data = userSearchesOverTimeResponse.data.map(item => item.count);
                }
                state.loading = false;
            } catch (error) {
                console.error(error);
                alert('Failed to load statistics');
            }
        });

        return state;
    },
});
</script>

<style scoped>
.statistics {
    padding: 20px;
    background-color: white;
    border-radius: 8px;
}

.chart-container {
    margin-bottom: 30px;
}

h2 {
    color: rgba(8, 60, 44);
    margin-bottom: 25px;
}

h3 {
    color: rgba(8, 60, 44);
    margin-bottom: 20px;
}

p {
    font-size: 18px;
    color: black;
}
</style>