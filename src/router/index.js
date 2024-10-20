import { createRouter, createWebHashHistory } from 'vue-router'
import MainPage from '../views/MainPage.vue'
import ChooseTankView from '@/views/ChooseTankView.vue';
import ChooseMapView from '@/views/ChooseMapView.vue';


const routes = [
  { path: '/', component: MainPage },  
  { path: '/chooseTanks', component: ChooseTankView },  
  { path: '/chooseMap', component: ChooseMapView }      

  // { path: '/game', component: GamePage },      
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
