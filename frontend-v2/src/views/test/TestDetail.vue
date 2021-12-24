<template>
  <div>
    <Navbar></Navbar>
    <div class="test-detail">
      <h3>{{test.name}}</h3>
      <hr>
      <hr>
      <div v-for="(question, index) in test.questions" class="text-left ml-5">
        <h5><b>{{index + 1}}. {{question.title}}</b></h5>

        <div class="row">
          <div class="col-6">
            <p v-bind:class="question.options[0].is_true ? 'text-success text-decoration-underline' : ''">
              {{question.options[0].answer}}
            </p>
            <p v-bind:class="question.options[1].is_true ? 'text-success text-decoration-underline' : ''">
              {{question.options[1].answer}}
            </p>
          </div>
          <div class="col-6">
            <p v-bind:class="question.options[2].is_true ? 'text-success text-decoration-underline' : ''">
              {{question.options[2].answer}}
            </p>
            <p v-bind:class="question.options[3].is_true ? 'text-success text-decoration-underline' : ''">
              {{question.options[3].answer}}
            </p>
          </div>
        </div>

        <hr>
      </div>
    </div>

  </div>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import Navbar from '../../components/Navbar.vue';
import {ApiService} from "@/services/api.service";
import {Test} from "@/services/interfaces";


@Component({
  components: {Navbar}
})
export default class TestDetail extends Vue {
  api = new ApiService();
  test: Test | null = null;
  async mounted(){
    let response = await this.api.getTest(this.$route.params.id);
    this.test = response.test;

  }



}
</script>

<style scoped>
.test-detail {
  padding-left: 10%;
  padding-right: 10%;
}
</style>