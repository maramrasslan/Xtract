import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state: {
    isAuthenticated: false,
    token: null,
  },
  mutations: {
    setAuthenticated(state, status) {
      state.isAuthenticated = status;
    },
    setToken(state, token) {
      state.token = token;
    },
  },
  actions: {
    async login({ commit }, payload) {
      try {
        const response = await axios.post('/api/login', {
          username: payload.username,
          password: payload.password,
        });
        const token = response.data.token;
        localStorage.setItem('token', token); // Store token in local storage
        commit('setAuthenticated', true);
        commit('setToken', token);
        return response.data; // Optionally return data if needed
      } catch (error) {
        console.error(error);
        throw error; // Propagate error to handle it in component
      }
    },
    logout({ commit }) {
      localStorage.removeItem('token'); // Remove token from local storage
      commit('setAuthenticated', false);
      commit('setToken', null);
    },
    setAuthenticated({ commit }, status) {
      commit('setAuthenticated', status);
    },
  },
});
