<template>
  <div class="mt-5">
    <div v-if="onLobby">
<!--  Waiting for players to join the game and configure  -->

      <b-alert variant="danger" v-model="wsError" show dismissible>
        Упс! Похоже у вас проблемы с интернетом или ошибка на сервере
      </b-alert>

      <div class="row">
        <div class="col-3">
          <p class="text-muted">Айди комнаты</p>
          <h3><strong>{{roomId}}</strong></h3>
          <hr>
          <h5><b>{{players.length}} игроков вошли</b></h5>
          <h6>{{ test.name }}</h6>
          <p>{{ test.questions.length }} вопросов</p>
          <hr>
          <h4><strong>Настройки</strong></h4>
          <p>Максимальное время</p>
          <input type="number" class="form-control" v-model="settings.maxTime">
          <br>
          <div class="form-check form-switch">
            <input type="checkbox" id="switch1"  v-model="settings.bonus">
            <label class="form-check-label" for="switch1">Давать бонусы за оставшееся время</label>
          </div>
          <br>
          <div class="form-check form-switch">
            <input type="checkbox" id="switch2" v-model="settings.showAnswers">
            <label class="form-check-label" for="switch2">Показать ответы в конце теста</label>
          </div>

        </div>

        <div class="col-6 text-left">
          <h4 v-for="player in players">{{player.name}}</h4>
        </div>

        <div class="col-3">
          <button class="btn btn-dark" v-on:click="startGame">Начать</button>
          <br><br>
          <button class="btn btn-danger">Выйти</button>
        </div>
      </div>
    </div>
    <div v-if="onGame">
      <div class="progress" style="height: 5px; margin-bottom: 10px">
        <div class="progress-bar bg-dark"
             role="progressbar"
             v-bind:style="{width: time + '%', height: '5px'}">
        </div>
      </div>
      <div class="row">
        <div class="col-3">

          <h5><b>Текущий вопрос: </b></h5> <br>
          <p>{{currentQuestion.title}}</p>
          <h5><b>Варианты ответа: </b></h5> <br>
          <p v-for="option in currentQuestion.options">{{option.answer}}</p>

        </div>
        <div class="col-6">
          <LeaderShip v-bind:players="players"></LeaderShip>
        </div>
        <div class="col-3">
          <button class="btn btn-dark" v-on:click="nextPermanently">Следующий вопрос</button>
        </div>
      </div>
    </div>
    <div v-if="onFinish">
      <Winners v-bind:winners="winners" v-bind:players="players.slice(3)"></Winners>
    </div>
  </div>


</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import LeaderShip from '@/components/LeaderShip.vue';
import Winners from "@/components/Winners.vue";

import {CreatorWS} from "@/services/websocket.service";
import {ApiService} from "@/services/api.service";

import {playerEvents} from "@/services/events";
import {Player, Question, Settings} from "@/services/interfaces";

@Component({
  components: {
    LeaderShip,
    Winners
  },
})
export default class Creator extends Vue {

  ws = new CreatorWS();
  api = new ApiService();

  roomId = 0;
  settings: Settings = {
    maxTime: 10,
    bonus: true,
    showAnswers: true
  }


  time = 100;
  test = {questions: [], name: ""};
  
  currentQuestion: Question | null = null;
  currentQuestionNumber: number = 0;
  
  players: Player[] = [];
  winners: Player[] = [];

  onLobby = true;
  onGame = false;
  onFinish = false;
  wsError = false;

  async beforeMount(){
      let response = await this.api.getTest(this.$route.params.id);
      if (response.status == 401) this.$router.push({"name": "login"});
      this.test = response.test;
  }

  async mounted(){

    // create game room and show room id
    let self = this;
    let response = await this.api.obtainRoomId();
    if (response.status == 401) this.$router.push({"name": "login"});

    this.ws.connectToRoom(response.room_id)
      .then(function (connection) {
        self.roomId = response.room_id;
        self.setEvents();
      })
      .catch(function (error) {
        self.wsError = true;
      })

  }

  startGame(){
    this.onLobby = false;
    this.onGame = true;
    this.ws.informPlayersToStartTheGame();
    this.ws.sendSettings(this.settings);

    this.api.closeRoom(this.roomId);

    this.nextQuestion();
    this.runQuestionAndTimerLoop();
  }

  setEvents(){
    let self = this;
    self.ws.setMessageEvent(function (message: any) {

      let data = JSON.parse(message.data);

      switch (data.event) {

        case playerEvents.JOIN_PLAYER: {

          let isFound = self.players.some(function (player: Player): any {
            if (player.name == data.name) return true;
          })

          if (!isFound){
            self.players.push({name: data.name, score: 0});
            self.ws.sendPlayers(self.players);
          }
          break;
        }

        case playerEvents.SEND_ANSWER: {
          self.addPointsToPlayer(data.player);
          self.sortPlayersByScore();
          self.ws.sendPlayers(self.players);
          break;
        }


      }

    })
  }

  addPointsToPlayer(player: Player){
    for (let i = 0; i < this.players.length; i++){

      if (this.players[i].name == player.name){
        this.players[i].score += player.score;
      }

    }
  }

  nextQuestion(){
    this.currentQuestion = this.test.questions[this.currentQuestionNumber];
    this.ws.sendQuestion(this.currentQuestion);
  }

  nextPermanently(){
    this.time = 0;
  }

  async runQuestionAndTimerLoop(){
    /**
    this method is responsible for sending questions every n seconds
    and finish the game if there are no questions left
    */
    this.time = 100;

    let unit = 10 / this.settings.maxTime;
    let intervalId: any = null;

    let func = ()=> {
      // if timeout
      if (this.time <= 0){

        if (this.currentQuestionNumber == this.test.questions.length - 1){
          this.finishTheGame();
          clearInterval(intervalId);
        } else {
          this.currentQuestionNumber++;
          this.nextQuestion();
          this.time = 100;
        }


      }
      this.time -= unit;
    };

    // call func every 100 milliseconds
    intervalId = setInterval(func, 100);
  }

  finishTheGame(){
    this.sortPlayersByScore();
    this.winners = this.players.slice(0, 3);

    this.onFinish = true;
    this.onGame = false;
    this.ws.sendWinnersAndFinish(this.winners);

    if (this.settings.showAnswers){
      this.ws.sendTestAnswers(this.test);
    }
  }

  sortPlayersByScore(){
    /**
     * decreasing sort like [{'score': 1}, {'score': 3}, {'score': 2}] =>
     * => [{'score': 3}, {'score': 2}, {'score': 1}]
     */
    this.players.sort(function (a, b) {
      return - (a.score - b.score);
    });

  }


}
</script>

<style lang="less">

</style>