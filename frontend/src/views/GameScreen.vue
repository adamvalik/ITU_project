<template>
  <div :style="{ width: `${gameWidth}px`, height: `${gameHeight}px`, backgroundColor: '#D5EFF4'}">
    <div>
      <div class="h-44 bg-opacity-80 bg-neutral-900 text-white items-center justify-center flex flex-rows space-x-8">

        <div class="flex flex-col space-y-1 w-1/3 relative">
          <div>
            <button
              @mouseover="showSelectorHelp"
              @mouseleave="hideSelectorHelp"
              @click="toggleWeaponMenu"
              class="h-16 w-full bg-blue-300 bg-opacity-50 text-black rounded-lg border-4 border-black hover:bg-blue-400 font-bold text-4xl relative">
              WEAPON SELECTOR
              <span v-if="selectorHelpVisible" class="absolute top-0 left-0 right-0 bottom-0 bg-black bg-opacity-50 flex justify-center items-center text-white text-2xl">
              Click to select weapon!
            </span>
            </button>
          </div>

          <div v-if="!toggleDropDownMenu">
            <button
              class="h-16 w-full bg-gray-300 bg-opacity-50 rounded-lg border-4 border-black hover:bg-gray-400">
              <div class="flex flex-row justify-center space-x-8">
                <div class="text-black font-bold text-3xl">{{ this.activeMissile.name }}</div>
                <div class="w-8 h-8" style="background: url('assets/small_missile_icon.png') no-repeat center center; background-size: cover;"></div>
                <div class="text-black font-bold text-3xl">{{ player1.ammunitionCount[activeMissile.id] }}</div>
              </div>
            </button>
          </div>

          <div v-if="toggleDropDownMenu" class="absolute top-full mt-2 bg-gray-600 border-4 border-gray-700 space-y-2">
            <button v-if="checkExistingAmmo('small')" @click="selectMissile('small')" class="h-16 w-full bg-gray-300 bg-opacity-50 rounded-lg border-4 border-black hover:bg-gray-400">
              <div class="flex flex-row justify-center space-x-8">
                <div class="text-black font-bold text-3xl">SMALL MISSILE</div>
                <div class="w-8 h-8" style="background: url('assets/small_missile_icon.png') no-repeat center center; background-size: cover;"></div>
                <div class="text-black font-bold text-3xl">{{ player1.ammunitionCount[0] }}</div>
              </div>
            </button>

            <button v-if="checkExistingAmmo('medium')" @click="selectMissile('medium')" class="h-16 w-full bg-gray-300 bg-opacity-50 rounded-lg border-4 border-black hover:bg-gray-400">
              <div class="flex flex-row justify-center space-x-8">
                <div class="text-black font-bold text-3xl">MEDIUM MISSILE</div>
                <div class="w-8 h-8" style="background: url('assets/small_missile_icon.png') no-repeat center center; background-size: cover;"></div>
                <div class="text-black font-bold text-3xl">{{ player1.ammunitionCount[1] }}</div>
              </div>
            </button>
            <button v-if="checkExistingAmmo('big')" @click="selectMissile('big')" class="h-16 w-full bg-gray-300 bg-opacity-50 rounded-lg border-4 border-black hover:bg-gray-400">
              <div class="flex flex-row justify-center space-x-8">
                <div class="text-black font-bold text-3xl">BIG MISSILE</div>
                <div class="w-8 h-8" style="background: url('assets/small_missile_icon.png') no-repeat center center; background-size: cover;"></div>
                <div class="text-black font-bold text-3xl">{{ player1.ammunitionCount[2] }}</div>
              </div>
            </button>
          </div>
        </div>

        <div class="relative w-1/4">
          <button
              @mouseover="showFireHelp"
              @mouseleave="hideFireHelp"
              @click="fireMissile"
              class="py-16 w-full bg-red-300 bg-opacity-50 text-black rounded-lg border-4 border-black hover:bg-red-400 font-bold text-4xl">
              FIRE
            <span v-if="fireHelpVisible" class="absolute top-0 left-0 right-0 bottom-0 bg-black bg-opacity-50 flex justify-center items-center text-white text-2xl">
              Click to fire!
            </span>
          </button>
        </div>

        <!-- Row flex for money, time and so on -->
        <div class ="flex flex-rows space-x-8 w-1/3 mt-4">

          <div class ="flex flex-col space-y-4 items-center">
            <div v-if="useTimer" class="font-bold text-white text-2xl">
              <h1>{{ timePerRound }} (s)</h1>
            </div>
            <div v-else class="font-bold text-white text-2xl">
              <h1>Inf</h1>
            </div>
            <div class = "w-16 h-16" style="background: url('assets/time_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

          <div class ="flex flex-col space-y-2 items-center">
            <div class="font-bold text-white text-2xl">
              <h1>{{ player1.money }}$</h1>
            </div>
            <div class = "w-20 h-20" style="background: url('assets/money_bag_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

          <div class ="flex flex-col space-y-2, items-center">
            <div class="font-bold text-white text-2xl">
              <h1>{{ player1.fuel }}/{{ player1.fuelMax }}</h1>
            </div>
            <div class = "w-20 h-20" style="background: url('assets/fuel_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

          <div class ="flex flex-col space-y-3 items-center">
            <div class="font-bold text-white text-2xl">
              <h1>{{ player1.wins }}win</h1>
            </div>
            <div class = "w-16 h-16" style="background: url('assets/trophy_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

          <div class="relative mb-16">
            <div class="w-20 h-20" style="background: url('assets/pause_icon.png') no-repeat center center; background-size: cover;"></div>
          </div>

        </div>
      </div>

    </div>

    <div>
      <canvas
        ref="gameCanvas"
        :width="canvasWidth"
        :height="canvasHeight"
        class="border border-gray-700 m-auto"
        @mousemove="onMouseMove"
        @click="onMouseClick"
        @mouseleave="onMouseLeave"
        @mouseup="onMouseUp"
        @mousedown="onMouseDown"
      ></canvas>
    </div>
    <div v-if="gameOver" class="absolute inset-0 flex flex-col space-y-2 items-center justify-center bg-black bg-opacity-50">
        <h1 class="text-4xl font-bold">You won!</h1>
        <button @click="backToMenu" class="border-4 border-sky-700 text-center bg-sky-300 hover:bg-sky-400 font-bold text-xl py-4 px-32 rounded-2xl mt-4 justify-center items-center">
          Back to Menu
        </button>

    </div>
  </div>
</template>

  <script>

  import axios from 'axios';
  export default {
    props: {
      gameWidth: Number,
      gameHeight: Number,
      scaleFactor: Number,
    },
    data() {
      return {
        //Default canvas size
        canvasWidth: this.gameWidth,
        canvasHeight: this.gameHeight - 176,

        //Map data
        terrain: [],
        terrainType: "",

        //Player data
        player1: {
          id: 0,
          name: "",
          tankType: 0,
          color: "",
          armorSkill: 0,
          powerSkill: 0,
          speedSkill: 0,
          skillPoints: 0,
          wins: 0,
          money: 0,
          fuel: 0,
          fuelMax: 0,
          health: 0,
          ammunitionCount: 0,
          xCord: 0,
          yCord: 0,
        },

        //Mouse position
        mousePosition: {
          x: 0,
          y: 0,
        },

        //Game data
        useTimer: false,
        timePerRound: 0,
        gameOver: false,
        wind: 0,

        //Aim circle data
        toggleHovering: false,
        toggleDragging: false,
        aimCircleRadius: 200,
        aimLaserXCord: 0,
        aimLaserYCord: 0,
        angle: 45,
        power: 50,

        //Missile trajectory data
        missileTrajectory: [],

        //Response
        responseGameOver: false,
        responseHitPlayer: false,
        responseMoney: 0,
        newterrain: [],
        newTargetHealth: 0,

        //Fire help visibility
        fireHelpVisible: false,
        selectorHelpVisible: false,
        toggleDropDownMenu: false,
        toggleDisableFire: false,

        //
        isPractice: true,
        practiceTarget: {
          name: "",
          xCord: 0,
          yCord: 0,
          health: 0,
          color: "",
        },

        activeMissile: {
          id: 0,
          name: "",
          damage: 0,
          radius: 0,
        }


      };
    },
    mounted() {
      this.selectActiveMissile('small');
      this.generateTerrain();
      this.loadPracticeTarget();
      this.loadPlayerData();
      this.loadGameData();
      window.addEventListener('keydown', this.onKeyPressed);
    },
    methods: {
      toggleWeaponMenu() {
        this.toggleDropDownMenu = !this.toggleDropDownMenu;
      },

      selectMissile(missileType) {
        this.selectActiveMissile(missileType);
        this.toggleDropDownMenu = false;
      },

      checkExistingAmmo(missileType) {
        if(missileType == 'small'){
          return this.player1.ammunitionCount[0] != -1;
        } else if(missileType == 'medium'){
          return this.player1.ammunitionCount[1] != -1;
        } else if(missileType == 'big'){
          return this.player1.ammunitionCount[2] != -1;
        }
      },

      selectActiveMissile(missileType) {
        if(missileType == 'small'){
          this.activeMissile = {
            id: 0,
            name: "SMALL MISSILE",
            damage: 20,
            radius: 30,
          };
        } else if(missileType == 'medium'){
          this.activeMissile = {
            id: 1,
            name: "MEDIUM MISSILE",
            damage: 30,
            radius: 40,
          };
        } else if(missileType == 'big'){
          this.activeMissile = {
            id: 2,
            name: "BIG MISSILE",
            damage: 40,
            radius: 50,
          };
        }
      },

      async loadPracticeTarget() {

        if(!this.isPractice){
          return;
        }

        await axios.get('http://localhost:8000/practice-target')
          .then((response) => {
            this.practiceTarget = response.data;
            this.drawGame();
          })
          .catch((error) => {
            console.error(error);
          });
      },

      async loadPlayerData() {
        await axios.get('http://localhost:8000/players/1')
          .then((response) => {
            this.player1 = response.data;
            console.log(response.data);
            this.drawGame();
          })
          .catch((error) => {
            console.error(error);
          });
      },

    async loadGameData() {
      await axios.get('http://localhost:8000/game')
        .then((response) => {
          this.useTimer = response.data.isTimer;
          this.timePerRound = response.data.timePerTurn;
          this.wind = response.data.wind;
          this.validateTimer();
        })
        .catch((error) => {
          console.error(error);
        });
    },

    validateTimer() {

      if(!this.useTimer){
        return;
      }

      setInterval(() => {
        if(this.timePerRound > 0) {
          this.timePerRound--;
        } else {
          this.gameOver = true;
        }
      }, 1000);
    },

      showFireHelp() {
        this.fireHelpVisible = true;
      },
      hideFireHelp() {
        this.fireHelpVisible = false;
      },

      showSelectorHelp() {
        this.selectorHelpVisible = true;
      },

      hideSelectorHelp() {
        this.selectorHelpVisible = false;
      },

      backToMenu() {
        this.$router.push('/');
      },

      calculateLaserPos() {
        const distance = (this.power / 100) * this.aimCircleRadius;
        const angleInRadians = (-this.angle * Math.PI) / 180;
        this.aimLaserXCord = this.player1.xCord + distance * Math.cos(angleInRadians);
        this.aimLaserYCord = this.player1.yCord + distance * Math.sin(angleInRadians);
      },


      drawPracticeTarget(ctx) {
        ctx.save();

        this.practiceTarget.yCord = this.terrain[Math.floor(this.practiceTarget.xCord)] - 40 / 2;

        const groundLevel = this.canvasHeight - 40 / 2;
        if (this.practiceTarget.yCord > groundLevel) {
            this.practiceTarget.yCord = groundLevel;
        }
        ctx.translate(this.practiceTarget.xCord, this.practiceTarget.yCord);

        //Color for outline
        ctx.strokeStyle = "black";

        // Draw the tank body
        ctx.fillStyle = this.practiceTarget.color;
        ctx.fillRect(-40 / 2, -40 / 4, 40, 40 / 2);
        ctx.strokeRect(-40 / 2, -40 / 4, 40, 40 / 2);

        // Draw the tank turret
        const turretLength = 40 * 0.7;
        ctx.translate(0, -40 / 7);
        ctx.rotate((-150 * Math.PI) / 180);
        ctx.fillStyle = this.practiceTarget.color;
        ctx.fillRect(0, -5, turretLength, 10);
        ctx.strokeRect(0, -5, turretLength, 10);
        ctx.restore();
      },

      drawPlayerNames(ctx) {
        ctx.save();
        //size of rectangles for healthbars
        const player1X = 10 + 200 / 2;
        const player2X = this.canvasWidth - 210 + 200 / 2;

        ctx.font = "28px Montserrat";
        ctx.fillStyle = "black";
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillText(this.player1.name, player1X, 30);
        if(this.isPractice){
          ctx.fillText(this.practiceTarget.name, player2X, 30);
        } else {
          ctx.fillText("Target", player2X, 30);
        }
        ctx.restore();
      },

      drawPlayerHealth(ctx){
        ctx.save();

        // Draw black fill
        ctx.fillStyle = 'black';
        ctx.fillRect(10, 50, 200, 40);
        ctx.fillRect(this.canvasWidth - 210, 50, 200, 40);

        // Draw red fill
        ctx.fillStyle = '#FF0000';
        const healthBarWidth = this.player1.health * 2;
        ctx.fillRect(10, 50, healthBarWidth, 40);

        if(this.isPractice){
          const practiceHealthBarWidth = this.practiceTarget.health * 2;
          ctx.fillRect(this.canvasWidth - 210, 50, practiceHealthBarWidth, 40);
        } else {
          ctx.fillRect(this.canvasWidth - 210, 50, 180, 40);
        }

        //Draw outline
        ctx.strokeStyle = 'gray';
        ctx.lineWidth = 5; // Border width
        ctx.strokeRect(10, 50, 200, 40);
        ctx.strokeRect(this.canvasWidth - 210, 50, 200, 40);

        ctx.fillStyle = '#FFFFFF'; // Text color
        ctx.font = '20px Montserrat';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(`${this.player1.health}/100`, 110, 70);

        if(this.isPractice){
          ctx.fillText(`${this.practiceTarget.health}/100`, this.canvasWidth - 110, 70);
        } else {
          ctx.fillText('80/100', this.canvasWidth - 110, 70);
        }

        ctx.restore();
      },

      drawWind(ctx){
        ctx.save();

        ctx.fillStyle = 'black'; // Text color
        ctx.font = 'bold 20px Montserrat';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('Wind: ', this.canvasWidth/2, 20);
        ctx.fillText(this.wind, this.canvasWidth/2 + 40, 20);

        ctx.restore();
      },

      drawAnglePower(ctx) {
        ctx.save();
        ctx.fillStyle = 'black';
        ctx.font = 'bold 20px Montserrat';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(`${Math.round(this.angle)}°,`, this.player1.xCord - 10, this.player1.yCord - 180);
        ctx.fillText(this.power, this.player1.xCord + 26, this.player1.yCord - 180);
        ctx.restore();
      },

      async generateTerrain() {
        await axios.get('http://localhost:8000/generate-terrain', {
          params: {
            canvasWidth: this.canvasWidth,
            canvasHeight: this.canvasHeight,
          }
        })
        .then((response) => {
          this.terrain = response.data.data;
          this.terrainType = response.data.type;
        })
        .catch((error) => {
          console.error(error);
        });
      },

      async fireMissile() {

        if(this.toggleDisableFire){
          return;
        }
        this.toggleDisableFire = true;

        await axios.post('http://localhost:8000/save-current-player-data', {
          player: this.player1,
        })
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.error(error);
        });

        const ammunition = this.player1.ammunitionCount[this.activeMissile.id];
        if(ammunition <= 0){
          this.toggleDisableFire = false;
          return;
        }

        await axios.post('http://localhost:8000/compute-missile-data', {
          canvasWidth: this.canvasWidth,
          canvasHeight: this.canvasHeight,
          playerId: this.player1.id,
          terrain: this.terrain,
          angle: this.angle,
          power: this.power,
          wind: this.wind,
          weaponSelected: this.activeMissile.id,
          radius: this.activeMissile.radius,
          damage: this.activeMissile.damage,
          targetHealth: this.practiceTarget.health,
          targetXCord: this.practiceTarget.xCord,
          targetYCord: this.practiceTarget.yCord,
        })
        .then((response) => {
          console.log(response);
          this.player1.ammunitionCount[this.activeMissile.id] = response.data.ammunitionCount;
          this.missileTrajectory = response.data.missileTrajectory;
          this.newTerrain = response.data.newTerrain;
          this.responseGameOver = response.data.gameOver;
          this.newTargetHealth = response.data.targetHealth;
          this.responseHitPlayer = response.data.hitPlayer;
          this.responseMoney = response.data.playerMoney;
        })
        .catch((error) => {
          console.error(error);
        });

        if(this.missileTrajectory != null){
          this.animateMissile();
        }

      },
      animateMissile() {

        const [x, y] = this.missileTrajectory.shift();

        this.drawGame();

        const canvas = this.$refs.gameCanvas;
        const ctx = canvas.getContext("2d");
        ctx.beginPath();
        ctx.arc(x, y, this.activeMissile.damage / 4, 0, 2 * Math.PI);
        ctx.fillStyle = "red";
        ctx.fill();

        if(this.missileTrajectory.length > 0){
          requestAnimationFrame(this.animateMissile);
        } else {

          this.terrain = this.newTerrain;

          if(this.responseHitPlayer){
            this.practiceTarget.health = this.newTargetHealth;
            this.player1.money += this.responseMoney;
          }
          if(this.responseGameOver){
            this.gameOver = true;
          }
          this.toggleDisableFire = false;
          this.drawGame();
        }
      },
      drawTerrain(ctx) {
        ctx.beginPath();
        ctx.moveTo(0, this.canvasHeight);
        for (let x = 0; x < this.terrain.length; x++) {
          ctx.lineTo(x, this.terrain[x]);
        }
        ctx.lineTo(this.canvasWidth, this.canvasHeight);
        ctx.closePath();
        if(this.terrainType === "mud"){
          // ctx.fillStyle = "saddlebrown";
          ctx.fillStyle = "#0D8747";
        } else {
          ctx.fillStyle = "green";
          console.log(this.terrain.type);
        }

        ctx.fill();
      },

      onKeyPressed(event){
        if(event.key === 'd'){
          if(this.player1.fuel > 0 && this.player1.xCord <  this.canvasWidth - 25){
            this.player1.fuel -= 5;
            this.player1.xCord += 5;
            this.aimLaserXCord += 5;
          }
        } else if(event.key === 'a'){
          if(this.player1.fuel > 0 && this.player1.xCord > 25){
            this.player1.fuel -= 5;
            this.player1.xCord -= 5;
            this.aimLaserXCord -= 5;
          }
        } else if(event.key === 'ArrowRight'){
          this.power = Math.min(100, this.power + 1);
        } else if(event.key === 'ArrowLeft'){
          this.power = Math.max(1, this.power - 1);
        } else if(event.key === 'ArrowUp'){
          this.angle += 1;
        } else if(event.key === 'ArrowDown'){
          this.angle -= 1;
        } else if(event.key === ' '){
          this.fireMissile();
        }

        this.drawGame();
      },

      onMouseDown(event) {
        //Obtain mousePosition relative to the canvas
        const rect = this.$refs.gameCanvas.getBoundingClientRect();
        this.mousePosition.x = (event.clientX - rect.left)/this.scaleFactor;
        this.mousePosition.y = (event.clientY - rect.top)/this.scaleFactor;

        //Check if the click is within the aim circle
        if (this.toggleHovering) {

          //Start dragging in the circle
          this.toggleDragging = true;

          //Update aiming line start positions
          this.aimLaserXCord = this.mousePosition.x;
          this.aimLaserYCord = this.mousePosition.y;
        }
      },

      onMouseUp() {

        //Dragging is stopped
        this.toggleDragging = false;
      },

      onMouseMove(event) {

          //Obtain mousePosition relative to the canvas
          const rect = this.$refs.gameCanvas.getBoundingClientRect();
          this.mousePosition.x = (event.clientX - rect.left)/this.scaleFactor;
          this.mousePosition.y = (event.clientY - rect.top)/this.scaleFactor;

          //Calculate the distance between the tank and the mouse
          const dx = this.mousePosition.x - this.player1.xCord;
          const dy = this.mousePosition.y - this.player1.yCord;
          const distance = Math.sqrt(dx * dx + dy * dy);

          //Toggle hovering if the mouse is within the aim circle range
          this.toggleHovering = distance >= 1 && distance <= this.aimCircleRadius;
          if(!this.toggleHovering){
            return;
          }

          //Dragging is enabled
          if (this.toggleDragging) {

            //Update the power value
            this.power = Math.round((distance / this.aimCircleRadius) * 100);

            //Update the laser line stop positions and angle
            const angle = Math.atan2(dy, dx);
            this.aimLaserXCord = this.player1.xCord + distance * Math.cos(angle);
            this.aimLaserYCord = this.player1.yCord + distance * Math.sin(angle);
            this.angle = -(angle * 180) / Math.PI;
          }

          //Redraw the game with updated values
          this.drawGame();
      },

      onMouseClick(event) {

        //Obtain mousePosition relative to the canvas
        const rect = this.$refs.gameCanvas.getBoundingClientRect();
        this.mousePosition.x = (event.clientX - rect.left)/this.scaleFactor;
        this.mousePosition.y = (event.clientY - rect.top)/this.scaleFactor;

        //Calculate the distance between the tank and the mouse
        const dx = this.mousePosition.x - this.player1.xCord;
        const dy = this.mousePosition.y - this.player1.yCord;
        const distance = Math.sqrt(dx * dx + dy * dy);

        //Toggle hovering if the mouse is within the aim circle range
        this.toggleHovering = distance >= 1 && distance <= this.aimCircleRadius;

        if (this.toggleHovering) {

          //Update the angle and power values
          this.angle = -(Math.atan2(dy, dx) * 180) / Math.PI;
          this.power = Math.round((distance / this.aimCircleRadius) * 100);

          //Redraw the game with updated values
          this.drawGame();
        }
      },

      drawTank(ctx) {

        ctx.save();
        console.log(this.player1.xCord, this.player1.yCord, 40);
        this.player1.yCord = this.terrain[Math.floor(this.player1.xCord)] - 40 / 2;

        const groundLevel = this.canvasHeight - 40 / 2;
        if (this.player1.yCord > groundLevel) {
          this.player1.yCord = groundLevel;
        }

        ctx.translate(this.player1.xCord, this.player1.yCord);

        //Color for outline
        ctx.strokeStyle = "black";


        // Draw the tank body
        ctx.fillStyle = this.player1.color;
        ctx.fillRect(-40 / 2, -40 / 4, 40, 40 / 2);
        ctx.strokeRect(-40 / 2, -40 / 4, 40, 40 / 2);

        // Draw the tank turret
        const turretLength = 40 * 0.7;
        ctx.translate(0, -40 / 7);
        ctx.rotate((-this.angle * Math.PI) / 180);
        ctx.fillStyle = this.player1.color;
        ctx.fillRect(0, -5, turretLength, 10);
        ctx.strokeRect(0, -5, turretLength, 10);

        ctx.restore();
      },

      drawAimCircle(ctx) {
        ctx.beginPath();
        ctx.arc(this.player1.xCord, this.player1.yCord, this.aimCircleRadius, 0, 2 * Math.PI);
        // Fill the circle with a semi-transparent color
        ctx.fillStyle = 'rgba(128, 128, 128, 0.2)';
        ctx.fill();  // Fill first to apply transparency correctly

        // Stroke the border of the circle
        ctx.strokeStyle = "black";
        ctx.stroke();

        // Draw the power/shot line
        ctx.beginPath();
        ctx.moveTo(this.player1.xCord, this.player1.yCord);
        ctx.lineTo(this.aimLaserXCord, this.aimLaserYCord); // Use the updated stop positions
        ctx.strokeStyle = "red";
        ctx.stroke();
      },

      drawGame(){

        // Get the canvas context
        const canvas = this.$refs.gameCanvas;
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight);

        // Calculate the laser line's endpoint based on the updated angle and power
        this.calculateLaserPos();

        // Draw the terrain
        this.drawTerrain(ctx);

        // Draw player 1's tank
        this.drawTank(ctx, this.player1);

        //Draw practice target
        if(this.isPractice){
          this.drawPracticeTarget(ctx);
        }

        //Draw player names
        this.drawPlayerNames(ctx);

        //Draw player health
        this.drawPlayerHealth(ctx);

        //Draw wind
        this.drawWind(ctx);

        //Draw angle and power values in the circle
        this.drawAnglePower(ctx);

        // Draw the aim circle
        this.drawAimCircle(ctx);

      },
    },
    beforeUnmount() {
      window.removeEventListener('keydown', this.onKeyPressed);
    },
  };
  </script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

canvas {
  font-family: 'Montserrat', sans-serif;
}
</style>
