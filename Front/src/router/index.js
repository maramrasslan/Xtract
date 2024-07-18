// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import Services from '../views/Services.vue';
import SearchTwitter from '../views/SearchTwitter.vue';
import SearchFacebook from '../views/SearchFacebook.vue';
import SearchLinkedin from '../views/SearchLinkedin.vue';
import About from '../views/About.vue';
import Login from '../views/Login.vue';
import Signup from '../views/Signup.vue';
import Profile from '../views/Profile.vue';
import History from '../views/History.vue';
import SearchProfile from '../views/SearchProfile.vue';
import Statistics from '../views/Statistics.vue';

const routes = [
  { path: '/', name: 'Services', component: Services },
  { path: '/searchTwitter', name: 'SearchTwitter', component: SearchTwitter },
  { path: '/searchFacebook', name: 'SearchFacebook', component: SearchFacebook },
  { path: '/searchLinkedin', name: 'SearchLinkedin', component: SearchLinkedin },
  { path: '/About', name: 'About', component: About },
  { path: '/Login', name: 'Login', component:Login},
  { path: '/Signup', name: 'Signup', component:Signup},
  { path: '/Profile', name: 'Profile', component:Profile},
  { path: '/History', name: 'History', component:History},
  { path: '/searchProfile', name: 'SearchProfile', component: SearchProfile },
  { path: '/statistics', name: 'Statistics', component: Statistics},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
