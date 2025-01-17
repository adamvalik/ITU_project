<!-- File: ChooseTankView.vue -->
<!-- Author: Adam Valík (xvalik05) -->

<template>
  <div
    class="flex bg-cover bg-center"
    :style="{ width: `${gameWidth}px`, height: `${gameHeight}px`, backgroundImage: `url('/assets/bg2.png')` }"
  >
    <!-- Player 1-->
    <div v-if="!loading" class="w-1/2 flex flex-col items-center justify-center">

      <!-- name input -->
      <div class="flex flex-col mb-6 -mt-10">
        <label class="font-semibold text-gray-700 mb-1">Enter Name:</label>
        <input
          v-model="player1.name"
          type="text"
          placeholder="Player 1 Name"
          class="border border-gray-300 rounded-lg px-4 py-2 text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200"
        />
      </div>

      <!-- tank selector -->
      <tank-selector
        :defaultColor="player1.color"
        :defaultTankType="player1.tankType"
        @tank-selected="updateTankSelection(1, $event)"
        @color-selected="updateColorSelection(1, $event)"
      />

      <!-- skill selectors -->
      <div>
        <div class="flex items-center space-x-2 mb-2">
          <label class="font-semibold text-gray-700 text-lg">Remaining Skill Points:</label>
          <span class="font-bold text-yellow-500 px-2 py-1 text-2xl">
            {{ player1.skillPoints }}
          </span>
        </div>
        <skill-selector
          :currentLevel="player1.armorSkill"
          :freePoints="player1.skillPoints"
          image="/assets/armor-icon.png"
          name="Armor"
          @update-skill="updateSkillLevel(1, 'armor', $event)"
          @update-free-points="updateFreePoints(1, $event)"
        />
        <skill-selector
          :currentLevel="player1.powerSkill"
          :freePoints="player1.skillPoints"
          image="/assets/power-icon.png"
          name="Power"
          @update-skill="updateSkillLevel(1, 'power', $event)"
          @update-free-points="updateFreePoints(1, $event)"
        />
        <skill-selector
          :currentLevel="player1.speedSkill"
          :freePoints="player1.skillPoints"
          image="/assets/speed-icon.png"
          name="Speed"
          @update-skill="updateSkillLevel(1, 'speed', $event)"
          @update-free-points="updateFreePoints(1, $event)"
        />
      </div>
    </div>
    <div v-else class="w-1/2 font-semibold text-xl flex flex-col items-center justify-center">
      <p>Loading...</p>
    </div>

    <!-- ----------------------------------------------------------- -->

    <!-- Player 2 -->
    <div v-if="!loading" class="w-1/2 flex flex-col items-center justify-center">

      <!-- name input -->
      <div class="flex flex-col mb-6 -mt-10">
        <label class="font-semibold text-gray-700 mb-1">Enter Name:</label>
        <input
          v-model="player2.name"
          type="text"
          placeholder="Player 2 Name"
          class="border border-gray-300 rounded-lg px-4 py-2 text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200"
        />
      </div>

      <!-- tank selector -->
      <tank-selector
        @tank-selected="updateTankSelection(2, $event)"
        @color-selected="updateColorSelection(2, $event)"
        :is-flipped="true" :defaultColor="player2.color"
        :defaultTankType="player2.tankType"
      />

      <!-- skill selectors -->
      <div>
        <div class="flex items-center space-x-2 mb-2">
          <label class="font-semibold text-gray-700 text-lg">Remaining Skill Points:</label>
          <span class="font-bold text-yellow-500 px-2 py-1 text-2xl">
            {{ player2.skillPoints }}
          </span>
        </div>
        <skill-selector
          :currentLevel="player2.armorSkill"
          :freePoints="player2.skillPoints"
          image="/assets/armor-icon.png"
          name="Armor"
          @update-skill="updateSkillLevel(2, 'armor', $event)"
          @update-free-points="updateFreePoints(2, $event)"
        />
        <skill-selector
          :currentLevel="player2.powerSkill"
          :freePoints="player2.skillPoints"
          image="/assets/power-icon.png"
          name="Power"
          @update-skill="updateSkillLevel(2, 'power', $event)"
          @update-free-points="updateFreePoints(2, $event)"
        />
        <skill-selector
          :currentLevel="player2.speedSkill"
          :freePoints="player2.skillPoints"
          image="/assets/speed-icon.png"
          name="Speed"
          @update-skill="updateSkillLevel(2, 'speed', $event)"
          @update-free-points="updateFreePoints(2, $event)"
        />
      </div>
    </div>
    <div v-else class="w-1/2 font-semibold text-xl flex flex-col items-center justify-center">
      <p>Loading...</p>
    </div>


    <!-- footer buttons -->
    <div class="absolute bottom-4 left-0 right-0 flex justify-between px-8">
      <router-link to="/" class="px-6 py-3 bg-gray-500 text-white font-semibold rounded-lg hover:bg-gray-600 transition duration-200">
        Back to Main Page
      </router-link>

      <router-link to="/chooseMap" @click="finalizeData" class="px-6 py-3 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600 transition duration-200">
        Choose Map
      </router-link>
    </div>
  </div>
</template>

<script>
import SkillSelector from '@/components/Selectors/SkillSelector.vue';
import TankSelector from '@/components/Selectors/TankSelector.vue';
import apiClient from '@/api';

export default {
  components: {
    TankSelector,
    SkillSelector
  },
  props: {
    gameWidth: Number,
    gameHeight: Number,
  },
  data() {
    return {
      loading: true,
      player1: {},
      player2: {},
    };
  },
  async mounted() {
    await this.fetchData();
  },
  watch: {
    'player1.name'(newValue) {
      if (newValue) this.updatePlayerName(1, newValue);
    },
    'player2.name'(newValue) {
      if (newValue) this.updatePlayerName(2, newValue);
    },
  },
  methods: {
    // dynamically update the player settings in the database on change
    async updatePlayerName(player, name) {
      try {
        await apiClient.post('/player/name', { player: player, name: name });
      } catch (error) {
        console.error(error);
      }
    },
    async updateTankSelection(player, tankType) {
      try {
        await apiClient.post('/player/tankType', { player: player, tankType: tankType });
      } catch (error) {
        console.error(error);
      }
    },
    async updateColorSelection(player, color) {
      try {
        await apiClient.post('/player/color', { player: player, color: color });
      } catch (error) {
        console.error(error);
      }
    },
    async updateSkillLevel(player, skill, value) {
      try {
        await apiClient.post('/player/skill', { player: player, skill: skill, value: value });
        await this.fetchData();
      } catch (error) {
        console.error(error);
      }
    },
    async updateFreePoints(player, skillPoints) {
      try {
        await apiClient.post('/player/skillPoints', { player: player, skillPoints: skillPoints });
        await this.fetchData();
      } catch (error) {
        console.error(error);
      }
    },

    // fetch the players data from the database
    async fetchData() {
      try {
        const response = await apiClient.get('/players');
        const players = response.data;

        if (players[0]) {
          this.player1 = players[0];
        }
        if (players[1]) {
          this.player2 = players[1];
        }

        this.loading = false;
      } catch (error) {
        console.error(error);
        this.loading = false;
      }
    },

    finalizeData() {
      // default values, if the user did not enter any name
      if (!this.player1.name) {
        this.updatePlayerName(1, "Player 1");
      }
      if (!this.player2.name) {
        this.updatePlayerName(2, "Player 2");
      }
    },
  }
}
</script>
