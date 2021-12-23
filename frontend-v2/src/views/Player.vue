<template>
  <div class="main-player">
    <br><br><br><br>
    <div v-if="websocketError">
      <b-alert show dismissible variant="danger">
        Вы ввели неправильный айди комнаты или у вас плохое соединение <br>
        попробуйте ещё раз
      </b-alert>
    </div>
    <div v-if="onLogin" class="ml-5 mr-5">
      <h3>Готовы играть!</h3>
      <p class="text-muted">Твоё имя</p>
      <input type="text" v-model="name" class="form-control">
      <p class="text-muted">Айди игры к которому ты хочешь присоединиться</p>
      <input type="number" v-model="roomId" class="form-control">
      <br>
      <button class="btn btn-outline-dark" v-on:click="enterTheGame">Играть</button>
    </div>
    <div v-if="onLobby">
      <h3><strong>Подождите пока другие игроки войдут</strong></h3>
      <b><i>Игроки</i></b>
      <h4 v-for="player in players">{{player.name}}</h4>
    </div>
    <div v-if="onQuestion">
      <h5>{{ question.title }}</h5>
      <hr>
      <div class="progress" style="height: 5px; margin-bottom: 10px">
        <div class="progress-bar bg-dark"
             role="progressbar"
             v-bind:style="{width: time + '%', height: '5px'}">
        </div>
      </div>
      <hr>
      <div class="row">
        <div class="col-6">
          <button class="btn btn-outline-dark answer" v-on:click="answer(question.options[0])">
            {{ question.options[0].answer }}
          </button>
          <br>
          <button class="btn btn-outline-dark answer" v-on:click="answer(question.options[1])">
            {{ question.options[1].answer }}
          </button>
        </div>
        <div class="col-6">
          <button class="btn btn-outline-dark answer" v-on:click="answer(question.options[2])">
            {{ question.options[2].answer }}
          </button>
          <br>
          <button class="btn btn-outline-dark answer" v-on:click="answer(question.options[3])">
            {{ question.options[3].answer }}
          </button>
        </div>
      </div>
    </div>
    <div v-if="onLeaderShip">
      <LeaderShip v-bind:players="players"></LeaderShip>
    </div>
    <div v-if="onFinish">
      <router-link to="/" class="btn btn-danger">Выйти</router-link>

      <button v-if="settings.showAnswers"
              v-on:click="onTestAnswers = true"
              class="btn btn-dark">
        Посмотреть ответы
      </button>

      <h1>Победители!</h1>
      <h1 v-for="player in winners">
        <b>{{player.name}}</b>
      </h1>
    </div>

    <div v-if="onTestAnswers">
      <router-link to="/" class="btn btn-danger">Выйти</router-link>
      <div v-for="question in test.questions">
        <p><b>{{question.title}}</b></p>
        <p v-for="option in question.options"
           v-bind:class="question.options[0].is_true ? 'text-success text-decoration-underline' : ''">
          {{option.answer}}
        </p>
      </div>
    </div>

    <div v-if="onTrueAnswerScreen" class="true-answer-screen">
      <h1>Правильно!</h1>
    </div>
    <div v-if="onFalseAnswerScreen" class="false-answer-screen">
      <h1 style="color: aliceblue">Неправильно :(</h1>
    </div>

  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import LeaderShip from "@/components/LeaderShip.vue";

import {PlayerWS} from "@/services/websocket.service";
import {Player, Settings, Question, Option, Test} from "@/services/interfaces";
import {creatorEvents} from "@/services/events";


@Component({
  components: {LeaderShip}
})
export default class Participant extends Vue {
  ws = new PlayerWS();

  onLogin = true;
  onLobby = false;
  onQuestion = false;
  onLeaderShip = false;
  onFinish = false;
  onTestAnswers = false;

  onTrueAnswerScreen = false;
  onFalseAnswerScreen = false;
  answerScreenTime = 1500;

  name = "";
  score = 0;

  roomId = 0;
  players: Player[] = [];
  winners: Player[] = [];

  test: Test | null = null;
  question: Question | null = null;

  settings: Settings = {
    maxTime: 10,
    bonus: true,
    showAnswers: true
  }

  time = 0;

  websocketError = false;

  async enterTheGame(){

    let self = this;

    this.ws.joinToRoom(this.roomId, this.name)
        .then(function (response) {
          self.setEvents();
          self.onLogin = false;
          self.onLobby = true;
        })
        .catch(function (error) {
          console.log(error);
          self.websocketError = true;
        })
  }

  setEvents(){
    let self = this;
    self.ws.setMessageEvent(function (message: any) {

      let data = JSON.parse(message.data);

      switch (data.event) {
        case creatorEvents.SEND_PLAYERS: {
          self.players = data.players;
          break;
        }

        case creatorEvents.SEND_SETTINGS: {
          self.settings = data.settings;
          break;
        }

        case creatorEvents.START_GAME: {
          self.onQuestion = true;
          self.onLobby = false;
          break;
        }

        case creatorEvents.SEND_QUESTION: {
          self.onQuestion = true;
          self.onLeaderShip = false;
          self.question = data.question;
          self.startTimer();
          break;
        }

        case creatorEvents.FINISH_GAME: {
          self.winners = data.winners;
          self.onFinish = true;
          self.onLeaderShip = false;
          self.onLobby = false;
          self.ws.closeConnection();
          break;
        }

        case creatorEvents.SEND_TEST_ANSWERS: {
          self.test = data.test;
          self.onFinish = false;
          self.onTestAnswers = false;
          break;
        }
      }
    })
  }

  async startTimer(){
    this.time = 100;

    let unit = 10 / this.settings.maxTime;
    let intervalId: any = null;

    let func = ()=> {
      if (this.time <= 0){
        this.sendAnswer();
        clearInterval(intervalId);
      }
      this.time -= unit;
    };

    intervalId = setInterval(func, 100);
  }

  answer(option: Option){
    if (option.is_true){
      this.score = 100;
      if (this.settings.bonus){
        this.score += this.time;
      }
      this.sendAnswer();
      this.onTrueAnswerScreen = true;
      setTimeout(() => {this.onTrueAnswerScreen = false}, this.answerScreenTime);
    }
    else {
      this.sendAnswer();
      this.onFalseAnswerScreen = true;
      setTimeout(() => {this.onFalseAnswerScreen = false}, this.answerScreenTime);
    }

    this.score = 0;
    this.onQuestion = false;
    this.onLeaderShip = true;
  }

  sendAnswer(){
    this.ws.sendAnswer({name: this.name, score: this.score});
  }

}
</script>

<style lang="less">
.answer {
  width: 90%;
  height: 100px;
  margin: 10px;
}

.screen {
  position: fixed;
  width: 100%;
  height: 100%;
  left: 0;
  top: 0;
  z-index: 10;
  text-align: center;
}

.true-answer-screen {
  .screen();
  background-color: white;
  h1 {
    margin-top: 20%;
  }
}

.false-answer-screen {
  .screen();
  background-color: black;
  h1 {
    margin-top: 20%;
  }
}

</style>
