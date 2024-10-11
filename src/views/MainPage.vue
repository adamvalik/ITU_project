<template>
  <div class="flex flex-col items-center justify-center h-screen bg-gray-100">
    <h1 class="text-4xl font-bold text-gray-800 mb-8">TANKY</h1>
    <RiveAnimation 
      src="tanks.riv"
      :width="390"
      :height="105"
      :autoplay="true"
    />
   
  </div>
</template>

<script>
import RiveAnimation from '../components/RiveAnimation.vue';

export default {
  name: 'MainPage',
  components: {
    RiveAnimation,
  },
  data() {
    return {
      showModal: false,
      color: '#00ff00'
    };
  },
  methods: {
    goTo(page) {
      this.showModal = false;
      this.$router.push({ path: `/${page}`, query: { color: this.color } });
    },
    closeModal() {
      this.showModal = false;
    }
  }
};
</script>

<style scoped>
/* Optional styling for the main page */
</style>
