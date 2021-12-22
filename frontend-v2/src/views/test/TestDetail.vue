<template>
  <div>
    <Navbar></Navbar>
    <h3>{{test.name}}</h3>
    <div v-for="question in test.questions" class="text-left ml-5">
      <h4><b>{{question.title}}</b></h4>
      <div v-for="option in question.options">
        <p v-bind:class="option.is_true ? 'text-success text-decoration-underline' : ''">
          {{option.answer}}
        </p>
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

</style>