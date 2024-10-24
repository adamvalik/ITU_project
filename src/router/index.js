import { createRouter, createWebHashHistory } from 'vue-router'
import MainPage from '../views/MainPage.vue'
import ChooseTankView from '@/views/ChooseTankView.vue';
import ChooseMapView from '@/views/ChooseMapView.vue';
import MapCreator from "@/views/MapCreator.vue";


const routes = [
  { path: '/', component: MainPage },  
  { path: '/chooseTanks', component: ChooseTankView },  
  { path: '/chooseMap', component: ChooseMapView },
  { path: '/mapCreator', component: MapCreator }

  // { path: '/game', component: GamePage },      
];

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
