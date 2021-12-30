<template>
  <div class="test-create">

    <Navbar></Navbar>

    <div v-if="error">
      <b-alert show dismissible variant="danger">
        Не удалось создать тест :( Наверное плохое соединение или проблемы на сервере
      </b-alert>
    </div>

    <input
      class="form-control"
      placeholder="имя теста"
      required
      v-model="test.name"
    >
    <hr>

    <button class="btn btn-dark" v-on:click="sendTest">Создать тест</button>
    <br>
    <div class="row">
      <div class="col-6">
            <!--  Question input  -->
        <div>
          <input class="form-control" placeholder="вопрос" required v-model="currentQuestionTitle">

          <hr>


              <input class="form-control" placeholder="вариант 1" required v-model="options[0].answer">
              <input type="radio" id="option0" value=0 v-model="correctOption" class="isTrue">
              <label for="option0">ответ</label>

              <input class="form-control" placeholder="вариант 2" required v-model="options[1].answer">
              <input type="radio" id="option1" value=1 v-model="correctOption" class="isTrue">
              <label for="option1">ответ</label>

              <input class="form-control" placeholder="вариант 3" required v-model="options[2].answer">
              <input type="radio" id="option2" value=2 v-model="correctOption" class="isTrue">
              <label for="option2">ответ</label>

              <input class="form-control" placeholder="вариант 4" required v-model="options[3].answer">
              <input type="radio" id="option3" value=3 v-model="correctOption" class="isTrue">
              <label for="option3">ответ</label>
          <br>

          <button class="btn btn-outline-dark" v-on:click="addQuestion">Добавить</button>
        </div>

      </div>
      <div class="col-6" style="overflow-y: scroll">
            <!--  Question list  -->

        <div >
          <div v-for="question in test.questions">
            <hr>
            <h5 class="text-center">{{question.title}}</h5>
            <div class="row">
              <div class="col-6">
                <b v-bind:class="question.options[0].is_true ? 'text-success text-decoration-underline' : ''">{{question.options[0].answer}}</b> <br>
                <b v-bind:class="question.options[1].is_true ? 'text-success text-decoration-underline' : ''">{{question.options[1].answer}}</b> <br>
              </div>
              <div class="col-6">
                <b v-bind:class="question.options[2].is_true ? 'text-success text-decoration-underline' : ''">{{question.options[2].answer}}</b> <br>
                <b v-bind:class="question.options[3].is_true ? 'text-success text-decoration-underline' : ''">{{question.options[3].answer}}</b> <br>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Navbar from '../../components/Navbar.vue';
import {Option, Test} from '@/services/interfaces';
import {ApiService} from "@/services/api.service";

@Component({
  components: {Navbar}
})
export default class TestCreate extends Vue {
  test: Test = {
    name: "",
    questions: []
  };

  currentQuestionTitle: string = "";
  correctOption: number = 0;

  options: Option[] = [
    {answer: "", is_true: false},
    {answer: "", is_true: false},
    {answer: "", is_true: false},
    {answer: "", is_true: false},
  ]

  error = false;

  api = new ApiService();

  addQuestion() {

    let self = this;

    this.options.forEach(function (option, index) {
      if (index == self.correctOption){
        option.is_true = true;
      }
    })

    this.test.questions.push({
      title: self.currentQuestionTitle,
      options: JSON.parse(JSON.stringify(self.options)) //deep copy
    })

    self.currentQuestionTitle = "";

    this.options.forEach(function (option) {
      option.is_true = false;
      option.answer = "";
    })
  }

  async sendTest() {
    let response = await this.api.createTest(this.test);
    if (response.status == 201){
      this.$router.push({'name': 'testList'});
    } else {
      this.error = true;
    }

  }

}
</script>

<style scoped>
.test-create {
  padding-left: 8%;
  padding-right: 8%;
}
</style>
