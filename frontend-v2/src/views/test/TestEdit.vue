<template>
  <div>
    <input type="text" v-model="test.name" class="form-control">
    <hr>
    <div v-for="question in test.questions">
      <input type="text" v-model="question.title" class="form-control">

      <div v-for="option in question.options">
        <input type="text"
               v-model="option.answer"
               v-bind:class="option.is_true ? 'text-success text-decoration-underline' : ''"
               class="form-control">
      </div>
    </div>
  </div>
</template>

<script lang="ts">

import {Vue, Component} from 'vue-property-decorator';
import {Test} from "@/services/interfaces";

import {ApiService} from "@/services/api.service";
import {Question} from "@/services/interfaces";

interface QuestionAnswers {
  correctOptionId: number;
  question: Question
}

@Component
export default class TestEdit extends Vue {

  test: Test = {name: "", questions: []};
  api: ApiService = new ApiService();

  questionsAnswers: QuestionAnswers[] = [];

  async mounted(){
    let response = await this.api.getTest(this.$route.params.id);
    this.test = response.test;

    let self = this;

    this.test.questions.forEach(function (question) {

      question.options.forEach(function (option){
        if (option.is_true){
          self.questionsAnswers.push({
            correctOptionId: question.options.indexOf(option),
            question: question
          })
        }
      })

    })

  }


}
</script>

<style scoped>

</style>