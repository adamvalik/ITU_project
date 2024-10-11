import { createRouter, createWebHashHistory } from 'vue-router'
import MainPage from '../views/MainPage.vue'

const routes = [
  { path: '/', component: MainPage },        
  // { path: '/game', component: GamePage },      
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
